# Description

REST API app created in Django that allows the user to upload and access images in JPEG and PNG format as well as access their thumbnails. Number and heights of the thumbnails depends on user account plan. There are 3 default plans (Basic, Premium, Enterprise), however the admin user can add additional custom plans.

After setting up the project (see Setup below), there are 3 main endpoints:
- http://127.0.0.1:8000/api/v1/images/ - At this endpoint authenticated users can upload and list images and see links to original image files and thumbnails, as well as view uuid numbers for detailed lookups.

- http://127.0.0.1:8000/api/v1/images/uuid:uuid/ - where **{uuid:uuid}** is the unique uuid of the image objects created by the user. At this endpoint authenticated users can view and delete a particular image.

- http://127.0.0.1:8000/api/v1/images/uuid:uuid/generate-link/int:expiry_time/ - where **\{uuid:uuid\}** is the unique uuid of the image objects created by the user, and **\{int:expiry_time\}** is the desired time for a link to expire. At this endpoint users can generate expiring links to their images (by default available to Enterprise plan only), that can then be accessed without the need to authenticate.

## Setup

You will need Docker installed to run app locally. 
To install Docker, follow instructions on [official Docker documentation](https://docs.docker.com/get-docker/ "Docker Documentation").

When you have Docker installed, follow these steps:


1. Clone the project:

```bash
  git clone https://github.com/ankurahuja-tech/images_thumbnails_project.git
```

2. Go to the project directory:

```bash
  cd images_thumbnails_project
```

3. Create local .env file:

```bash
  cp ./.env.example.dev ./.env
```

4. Build docker image and run docker containers (web and db) in detached mode:

```bash
  docker-compose up -d --build
```

5. Finally navigate to http://127.0.0.1:8000/api/v1/images/ or http://127.0.0.1:8000/admin in your browser and verify that the app is running.

6. To use Admin Panel at http://127.0.0.1:8000/admin, create admin user:

```bash
  docker-compose exec web python manage.py createsuperuser
```

7. After finishing using the app, stop and remove containers ("-v" flag also removes volumes): 

```bash
docker-compose down -v
```

### Running tests:

To run tests, run the following command while the docker containers are running:

```bash
docker-compose exec web pytest -v --ds=config.settings.test
```

### Basic troubleshooting:

If the app isn't working after running the docker containers (see step 4), verify that the containers (web and db) are in fact running:

```bash
  docker ps
```

If the containers are running, verify that the Django app within the container is running:

```bash
  docker-compose logs -f
```

## Author

[@ankurahuja-tech](https://www.github.com/ankurahuja-tech)

  
## License

[MIT](https://choosealicense.com/licenses/mit/)
