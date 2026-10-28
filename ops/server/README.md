# InceptionV1 独立服务器部署

本包包含完整线上第 6 版的网页和运行资源，不包含 Git 历史及原始备份图片。无需 Node.js、Python、GPU、GPT API 或 ChatGPT 登录。Nginx 负责提供静态文件。原始研究站的链接仅供点击查看来源。

## 当前状态

尚未安装到服务器：执行环境对 `47.100.101.127:22` 返回 `Network is unreachable`，未进入密码验证阶段。不能据此判断服务器是否停机、密码是否正确或安全组是否放行。

## 安装

先把下载的 `inception-server-deploy.tar.gz` 放到自己电脑的当前目录，在该电脑的终端运行：

```sh
scp inception-server-deploy.tar.gz root@47.100.101.127:/root/
ssh root@47.100.101.127
```

密码由 SSH 在终端中交互询问。本包不保存密码。

进入服务器后运行：

```sh
mkdir -p /root/inception-deploy
tar -xzf /root/inception-server-deploy.tar.gz -C /root/inception-deploy
cd /root/inception-deploy
bash install.sh
curl -I http://127.0.0.1/ -H 'Host: 47.100.101.127'
```

脚本支持有 apt-get、dnf 或 yum 的 Linux，要求 root 权限。会在缺失时安装 Nginx；新增独立配置；保留已有网站配置和历史发布目录。若 80 端口被其他非 Nginx 服务占用则停止，可以改用 `PORT=8080 bash install.sh`。服务器系统、现有服务、软件源和防火墙尚未经远程确认，首次实际安装仍需验证。

云安全组和服务器防火墙需允许所选 HTTP 端口。脚本不擅自修改防火墙。安装成功后公网地址为 `http://47.100.101.127/#level=1`（若改为 8080，需要加 `:8080`）。这只是预期地址，目前尚未验收可访问。

## 缓存与数据

图片与压缩数据设置 24 小时浏览器缓存；HTML、JavaScript、CSS 重新验证版本。AVIF 图片已压缩；JSON 和热图采用无损 gzip，并由网页代码主动解压，因此不要额外给显式 `.gz` 文件添加 `Content-Encoding: gzip`。

新服务器不受原托管发布包体积限制，以后可另行升级为原始高清资源。当前包保留线上版的图像尺寸和隐藏标记，不凭迁移就声称提速。应从实际用户网络测量第三、四级首次加载及重复加载耗时；CPU 较低不一定是静态站瓶颈，公网带宽和网络延迟仍可能限制速度。

## 域名与 HTTPS

可以绑定你持有的域名，把 DNS 指向服务器，再配置 HTTPS。尚未提供域名，因此本包没有更改 DNS 或申请证书。`chatgpt.site` 是原托管地址；它的名称不意味着网页运行依赖 GPT。`honeysugar12` 是原地址中的子域名，仅凭地址无法确定其命名来源。

## 回退

脚本会输出旧版本目录；如有旧版本，可以将 `/var/www/inception-microscope/current` 符号链接指回该目录，并执行 `nginx -t && systemctl reload nginx`。已有站点配置会保留时间戳备份。请保留压缩包和安装输出，便于后续核查。
