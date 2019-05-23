# Redash 中文化

对Redash部分界面进行中文化，调查后暂时发现三处需汉化的模块

- [ ] I ~~Angular i18n (涉及细节较多，且官方正在向React迁移，暂不汉化)~~
- [x] I plotly.js (报表相关)
- [x] I moment (日期相关)
- [ ] I Flask-Babel, 后端代码的国际化，但 Redash 并没有集成。
  - [官方文档](https://pythonhosted.org/Flask-Babel/)
  - 查找待翻译的内容```bash pybabel extract -F babel.cfg -o messages.pot ..```
  - 初始化中文翻译```bash pybabel init -i messages.pot -d translations -l zh```
  - 编译```bash pybabel compile -d .```
  - 每次更新待翻译的内容```bash pybabel update -i messages.pot -d .```
- [ ] I React intl, 前端 React 部分的国际化
- [ ] I Angular, [参考此处](https://angular.io/guide/i18n)
