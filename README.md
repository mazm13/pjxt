# PJXT
## Requirements
python 2.7，需要selenium和numpy两个python库，可以直接通过pip下载，如下
```bash
$ pip install selenium
$ pip install numpy
```

## Usage
可以通过修改89行的代码
```python
dates = datelist((2017, 12, 1), (2018, 1, 26))
```
来选择你需要评教的日期范围（记得保存哦）。通过
```bash
$ python main.py
```
启动程序后，会弹出一个浏览器并显示登录界面，手动输入账号密码及验证码后点击登录，这时在程序界面输入```1```并回车，这时浏览器会自动完成评教！（注：已评教的课程会被自动跳过）

## License
This project is licensed under the MIT License