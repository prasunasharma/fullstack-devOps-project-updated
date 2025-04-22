terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "fastapi" {
  name         = "tiangolo/uvicorn-gunicorn-fastapi:python3.9"
  keep_locally = false
}

resource "docker_container" "fastapi" {
  name  = "fastapi-demo"
  image = docker_image.fastapi.name

  ports {
    internal = 80
    external = 8080
  }
}
