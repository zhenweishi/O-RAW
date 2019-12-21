docker rmi jvsoest/oraw
docker build -t jvsoest/oraw ./

@echo off
:Ask
set ANSWER=
set /P ANSWER=Upload jvsoest/oraw to Docker Hub? (y/N) %=%
If "%ANSWER%"=="y"  goto yes 
If "%ANSWER%"=="Y" goto yes

goto end

:yes
echo "Uploading to Docker Hub"
docker push jvsoest/oraw

:end
echo "Done."