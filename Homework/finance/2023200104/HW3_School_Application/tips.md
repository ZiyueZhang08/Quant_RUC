# Tips

Excellent work!

Some suggestions:

- The micro-scripts (`update_gpa_xx.py`) could be combined into a single script using `functions` (with a `str`) paremeter. For example:

```python
def update_gpa(grade):
    import json
    p = r"C:\Users\32854\Desktop\quant课\HW_School_Application\personal_info.json"
    with open(p,'r',encoding='utf-8-sig') as f:
        d = json.load(f)
    d['gpa'] = grade
    with open(p,'w',encoding='utf-8') as f:
        json.dump(d,f,ensure_ascii=False,indent=2)
    print("GPA updated to", d['gpa'])
```

- You can have a more general function to combine all `update_xxx.py` scripts. 
