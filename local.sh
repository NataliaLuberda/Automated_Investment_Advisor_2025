docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=mydatabase -e MYSQL_USER=admin -e MYSQL_PASSWORD=supersecurepassword -p 3306:3306 -d mysql:latest
