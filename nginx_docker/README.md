1. To build docker image with latest tag:

        docker build -t nginx .
   else
	docker build -t <image_name>:<tag> .


2. To run nginx image:

	docker run -v /path to dir/ -p 80:80 -dt <image_id>
	
	NOTE : While runnuing nginx separately user needs to volume mount the nginx config directory. (Nginx config directory can be found in compose directory of nginx )
      
      If running through docker-compose file, no need to do separate volume mount as it is already done in docker-compose.yml. 
