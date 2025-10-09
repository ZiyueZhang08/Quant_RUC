import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from docxtpl import DocxTemplate
import os
from docx2pdf import convert

def fetchUniversityList():
    # 从网页读取学校列表信息
    url = "https://ideas.repec.org/top/top.econdept.html"
    resp = requests.get(url, timeout=20)
    resp.encoding = resp.apparent_encoding or 'utf-8'
    soup = BeautifulSoup(resp.text, "lxml")

    candidates = []
    for li in soup.select("ol li"):
        txt = li.get_text(" ", strip=True)
        if txt:
            candidates.append(txt)
    if not candidates:
        for tr in soup.select("table tr"):
            txt = tr.get_text(" ", strip=True)
            if txt:
                candidates.append(txt)
    if not candidates:
        full = soup.get_text("\n")
        candidates = re.findall(r'^\s*\d+\..+$', full, flags=re.M)

    # 提取网页的rank与institution部分
    rows = []
    for line in candidates:
        m = re.search(r'^\s*(\d+)\s+(.+?)\s+(-?\d+\.\d+)\s+\d+', line)
        if m:
            rank = int(m.group(1))
            instRaw = m.group(2).strip()
        else:
            m2 = re.search(r'^\s*(\d+)\s+(.+)$', line)
            if not m2:
                continue
            rank = int(m2.group(1))
            instRaw = m2.group(2).strip()
        rows.append({"rank": rank, "raw": instRaw})

    if not rows:
        raise RuntimeError("未能从页面提取有效排名行，请检查页面结构。")

    # 关键词与国家表（用于排除仅为国家的错误结果）
    instKeywords = [
        "University", "Institute", "College", "School", "Universiteit", "École",
        "Business School", "School of Economics", "School of Management", "School of Arts and Sciences"
    ]
    countries = {
        "netherlands","italy","france","spain","canada","china","germany","united kingdom",
        "united states","usa","australia","brazil","japan"
    }

    # 用于从文本中提取完整机构名的正则（尽量包含 "University of X" 和带连字符的校名）
    instPattern = re.compile(
        r'(?i)(.+?(?:University(?: of [A-Za-z\-\s&]+|-[A-Za-z0-9]+)?|Institute(?: of [A-Za-z\-\s&]+)?|College(?: of [A-Za-z\-\s&]+)?|School(?: of [A-Za-z\-\s&]+)?|Business School|School of Economics|School of Management|School of Arts and Sciences))',
        flags=re.I
    )

    def cleanInstitutionName(raw):
        # 去括号和多余空格
        s = re.sub(r'\(.*?\)', '', raw).strip()
        s = re.sub(r'\s{2,}', ' ', s)
        # 先按逗号分段，从后向前找包含关键词的段落
        parts = [p.strip() for p in s.split(',') if p.strip()]
        for part in reversed(parts):
            if any(kw.lower() in part.lower() for kw in instKeywords):
                # 在该段内用正则抓取机构部分（优先最长匹配）
                m = instPattern.search(part)
                if m:
                    candidate = m.group(1).strip().rstrip(' ,')
                else:
                    candidate = part
                # 如果candidate仅为国家名或非常短，尝试回退到前一段
                low = candidate.lower()
                if low in countries or len(candidate.split()) <= 1:
                    continue
                return candidate
        # 若逗号段未找到，尝试在整行匹配
        m = instPattern.search(s)
        if m:
            candidate = m.group(1).strip().rstrip(' ,')
            if candidate.lower() in countries or len(candidate.split()) <= 1:
                # 回退：取去掉系/院前缀后的剩余
                s2 = re.sub(r'^(Department of [^,]+,?|Economics Department,?|Dept\. of [^,]+,?)\s*', '', s, flags=re.I).strip()
                s2 = re.sub(r'\s*\(.*?\)', '', s2).strip()
                return s2 if s2 and s2.lower() not in countries else candidate
            return candidate
        # 最后保底：去掉开头的系/院前缀并取第一段
        s2 = re.sub(r'^(Department of [^,]+,?|Economics Department,?|Dept\. of [^,]+,?)\s*', '', s, flags=re.I).strip()
        s2 = re.sub(r'\s*\(.*?\)', '', s2).strip()
        if ',' in s2:
            s2 = s2.split(',')[0].strip()
        # 如果仍然是国家名，返回空字符串以便后续过滤
        if s2.lower() in countries:
            return ""
        return s2

    df = pd.DataFrame(rows).drop_duplicates(subset=["rank"]).sort_values("rank").reset_index(drop=True)
    df['clean'] = df['raw'].apply(cleanInstitutionName)

    # 仅保留 1-90 且 clean 非空
    df_1_90 = df[(df['rank'] >= 1) & (df['rank'] <= 90)].copy()
    df_1_90 = df_1_90[df_1_90['clean'].str.strip() != ""].reset_index(drop=True)

    # 选择：1-30 取 1-10，31-60 取 31-40，61-90 取 61-70
    selectedRanks = list(range(1, 11)) + list(range(31, 41)) + list(range(61, 71))
    dfSelected = df_1_90[df_1_90['rank'].isin(selectedRanks)].copy()
    dfSelected = dfSelected.drop_duplicates(subset=["clean"]).sort_values("rank").reset_index(drop=True)

    # 只保存最终选定的30所大学到universityList.xlsx
    dfSelected[['clean']].rename(columns={'clean': 'University'}).to_excel("universityList.xlsx", index=False)

    # 控制台输出检查
    print(f"Total rows parsed: {len(df)}; kept 1-90 (non-empty): {len(df_1_90)}; selected final: {len(dfSelected)}")
    print("\nSelected 30 universities:")
    for _, r in dfSelected.iterrows():
        print(f"{int(r['rank']):2d} - {r['clean']}")

    return dfSelected

def createResearchData():
    
    # 创建研究数据Excel文件
    # 研究方向和技术技能是预先手动从Glassdoor获取的

    # 预先手动从Glassdoor获取的研究方向和技术技能
    predefinedFieldsAndTechniques = {
        "Economics": {
            "technique1": "Proficiency in Microsoft Office",
            "technique2": "Highly developed analytical, research and written skills", 
            "technique3": "Advanced SQL skills"
        },
        "Finance": {
            "technique1": "Ability to quickly learn new technology",
            "technique2": "Excellent communication, time management skills",
            "technique3": "Strong computer skills with emphasis in time series"
        },
        "Management": {
            "technique1": "Interpersonal skills – ability to collaborate effectively in a team",
            "technique2": "Relevant coursework, internships, or extracurricular leadership experience",
            "technique3": "Excellent written and verbal communication"
        }
    }
    
    print("=== 预先定义的研究方向和技术技能 ===")
    for field, techniques in predefinedFieldsAndTechniques.items():
        print(f"{field}: {list(techniques.values())}")
    
    # 从网页爬取顶级期刊
    print("\n=== 开始从网页爬取顶级期刊 ===")
    journalsData = scrapeJournalsFromWeb()
    
    # 将期刊数据与预定义的研究方向和技能合并
    researchData = mergeJournalsWithFields(journalsData, predefinedFieldsAndTechniques)
    
    # 创建DataFrame并保存到Excel
    dataFrame = pd.DataFrame(researchData)
    outputFile = 'researchData.xlsx'
    dataFrame.to_excel(outputFile, index=False)
    
    print(f"\n=== 最终生成的研究数据 ===")
    print(dataFrame)
    print(f"\n数据已保存到 {outputFile}")
    
    return dataFrame

def scrapeJournalsFromWeb():
    # 从指定网页爬取顶级期刊信息
    
    url = "https://www.scmor.com/view/10554"
    
    try:
        # 发送HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"网页标题: {soup.title.string if soup.title else '无标题'}")
        
        # 查找所有可能的期刊列表
        journalElements = soup.find_all(['p', 'li', 'div', 'td'])
        
        # 提取所有可能的期刊名称
        possibleJournals = []
        for element in journalElements:
            text = element.get_text(strip=True)
            # 期刊名称通常包含"Journal"、"Review"等关键词，且长度适中
            if (len(text) > 5 and len(text) < 100 and 
                any(keyword in text.lower() for keyword in ['journal', 'review', 'economics', 'finance', 'management', 'accounting'])):
                possibleJournals.append(text)
        
        print(f"找到 {len(possibleJournals)} 个可能的期刊名称")
        
        # 按研究领域分类期刊
        categorizedJournals = categorizeJournals(possibleJournals)
        
        return categorizedJournals
        
    except Exception as e:
        print(f"爬取网页时出错: {e}")
        # 如果爬取失败，返回空数据
        return {
            "Economics": ["", "", ""],
            "Finance": ["", "", ""],
            "Management": ["", "", ""]
        }

def categorizeJournals(journals):
    # 将期刊按研究领域分类
    
    # 定义研究领域和对应的关键词
    fieldKeywords = {
        "Economics": ["economic", "econometric", "economy", "economic review", "political economy"],
        "Finance": ["finance", "financial", "investment", "banking", "capital", "portfolio"],
        "Management": ["management", "administrative", "strategic", "organization", "business", "leadership"]
    }
    
    categorizedJournals = {}
    
    for field, keywords in fieldKeywords.items():
        fieldJournals = []
        
        # 从网页期刊中匹配当前领域的期刊
        for journal in journals:
            # 检查期刊是否包含该领域的关键词
            if any(keyword in journal.lower() for keyword in keywords):
                # 避免重复添加
                if journal not in fieldJournals:
                    fieldJournals.append(journal)
        
        # 取前3个匹配的期刊，如果不足3个则用空字符串填充
        topJournals = fieldJournals[:3] if len(fieldJournals) >= 3 else fieldJournals + [""] * (3 - len(fieldJournals))
        
        categorizedJournals[field] = topJournals
        print(f"领域 '{field}' 匹配到 {len(fieldJournals)} 个期刊: {topJournals}")
    
    return categorizedJournals

def mergeJournalsWithFields(journalsData, fieldsAndTechniques):
    """
    将期刊数据与预定义的研究方向和技能合并
    """
    researchData = []
    
    for field, techniques in fieldsAndTechniques.items():
        # 获取该领域的期刊
        fieldJournals = journalsData.get(field, ["", "", ""])
        
        researchData.append({
            "field": field,
            "journal1": fieldJournals[0] if len(fieldJournals) > 0 else "",
            "journal2": fieldJournals[1] if len(fieldJournals) > 1 else "",
            "journal3": fieldJournals[2] if len(fieldJournals) > 2 else "",
            "technique1": techniques["technique1"],
            "technique2": techniques["technique2"],
            "technique3": techniques["technique3"]
        })
    
    return researchData

if __name__ == "__main__":
    # 主函数部分

    fetchUniversityList()
    createResearchData()
    # 读取学校数据
    universityDf = pd.read_excel('universityList.xlsx')
    universities = universityDf['University'].tolist()
    
    # 读取研究领域数据
    researchDf = pd.read_excel('researchData.xlsx')
    print(f"读取到 {len(researchDf)} 个研究领域")
    
    # 创建输出目录
    outputDir = 'AdmissionLetters'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        print(f"创建目录: {outputDir}")
    else:
        print(f"目录已存在: {outputDir}")
    
    # 加载模板
    template = DocxTemplate('admissionTemplate.docx')
    print("模板加载成功")
    
    # 外层循环 - 遍历大学
    i = 0
    while i < len(universities):
        university = universities[i]
        
        # 内层循环 - 遍历研究领域
        j = 0
        while j < len(researchDf):
            researchRow = researchDf.iloc[j]
            
            # 准备替换数据
            context = {
                'university': university,
                'field': researchRow['field'],
                'journal1': researchRow['journal1'],
                'journal2': researchRow['journal2'],
                'journal3': researchRow['journal3'],
                'technique1': researchRow['technique1'],
                'technique2': researchRow['technique2'],
                'technique3': researchRow['technique3']
            }
            
            # 生成文件名 - 修正这里
            safeUniversity = ''.join(c for c in university if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safeField = ''.join(c for c in researchRow['field'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safeUniversity}_{safeField}"
            docxPath = os.path.join(outputDir, f"{filename}.docx")  # 去掉filename中的.docx
            pdfPath = os.path.join(outputDir, f"{filename}.pdf")    # 去掉filename中的.pdf
            
            # 渲染并保存Word文档
            template.render(context)
            template.save(docxPath)
            
            # 立即导出PDF版本
            try:
                convert(docxPath, pdfPath)
                print(f"生成第 {i*len(researchDf) + j + 1} 封: {filename}.docx 和 {filename}.pdf")
            except Exception as e:
                print(f"生成第 {i*len(researchDf) + j + 1} 封: {filename}.docx (PDF转换失败: {e})")
            
            j += 1
        
        i += 1
    
    print("\n生成完成")
    print(f"成功生成 {len(universities) * len(researchDf)} 封申请信")
    print(f"文件保存在: {outputDir} 目录")
    print("\n注意: Glassdoor有Cloudflare反爬机制,所以technique字段是手动搜索的.")