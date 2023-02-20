# hexOceanBackend

## Docker compose
- Clone the repository
- Run: `docker compose up --build`

The app will be accessible through `localhost:8000`in Docker and on the local machine

Superuser credentials: `admin : DbUZ1Qe86qWcxWHJNsilmB`


## Manual setup
- Clone the repository
- Run: `pip install -r requirements.txt`
- Run: `python manage.py migrate`
- Run: `python manage.py createsuperuser` and create superuser
- Run: `python manage.py runserver`

The app will be accessible through `127.0.0.1:8000` on the local machine


## CLI
`python manage.py thumbnail_permission [--delete] [SIZE]` - Create/delete a permission for thumbnail size

`python manage.py runcrons` - Run all [CronJobs](https://django-cron.readthedocs.io/). Used to clean up expired images
that have not been deleted the other way

`python -m pytest tests/` - Run all tests


# API overview
| Path                                         | Method | Description                                                |
| -------------------------------------------- | ------ | ---------------------------------------------------------- |
| /api/                                        | GET    | API Overview                                               |
| /api/upload/                                 | POST   | Upload Image                                               |
| /api/delete/\<str:uuid\>/                    | DELETE | Delete Image with given UUID                               |
| /api/list/\<int:page\>/                      | GET    | List Images (Paged)                                        |
| /api/find/\<str:title\>/                     | GET    | Find Images                                                |
| /api/expiring/\<str:uuid\>/\<int:duration\>/ | GET    | Get expiring link to an Image with given UUID              |

## /api/upload/

Input (Multipart): 
```
{
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "image": {"type": "file"}
    },
    "required": [
        "title",
        "image"
    ]
}
```

Output:
```
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "uuid": {"type": "string"},
    "thumbnails": {
      ...
    },
    "original": {
      "type": "string"
    }
  },
  "required": [
    "title",
    "uuid"
  ]
}
```
