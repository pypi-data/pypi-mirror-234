import jinja2 as jj
import shutil as sh
import os
import json

res_dir = os.path.join(os.path.dirname(__file__),"..","data","poject")
def flask(path,name,author,site,license):
    PJ_path = os.path.join(path,name)
    PJ_port = int(input("默认端口："))
    PJ_config = {
        "Name":name,
        "Author":author,
        "Web Site":site
    }
    if os.path.exists(PJ_path):
        print("项目已存在")
        return
    else:
        PJ_res_dir = os.path.join(res_dir,"flask")
        sh.copytree(PJ_res_dir,PJ_path)
        # 渲染py模板
        out_py = jj.Template(open(os.path.join(PJ_path,"app.py")).read()).render(port=PJ_port)
        open(os.path.join(PJ_path,"app.py"),"w").write(out_py)
        config = json.dumps(PJ_config,indent=4,ensure_ascii=False)
        open(os.path.join(PJ_path,"config.json"),"w").write(config)
        print("项目创建成功")

        

    