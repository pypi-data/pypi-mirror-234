# easy-kubeflow

python sdk for kubeflow platform. use following func in .ipynb file

## install 
```bash
pip install -U easy-kubeflow
```

## docker

examples for use of docker

### initial

init docker client

Similar to cmd line ``docker login``

```python
from easy_kubeflow import EasyDocker
docker = EasyDocker()

2022-03-22 01:39:02.933 [INFO] Connected to host docker successfully !
```
### show images

show images in container's host node.

Similar to cmd line ``docker images | grep xxx``. when name none, show all images

```python
docker.show_images(grep="liuweibin")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:base	f621486595fe	2022-03-17T02:02:18.143	8.1 GB
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:test	8491b7b97d72	2022-01-21T10:13:34.857	8.1 GB
```

### pull images

pull images from service.stonewise.cn:5000/ or harbor or harbor proxy (recommend)

Similar to cmd line ``docker pull xxx``

```python
docker.pull_images(repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/3 [00:00<?, ?it/s]2022-03-22 01:53:12.543 [INFO] Pulling from proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount
 33%|███▎      | 1/3 [00:00<00:00,  9.84it/s]2022-03-22 01:53:12.646 [INFO] Digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4
 67%|██████▋   | 2/3 [00:00<00:00,  9.75it/s]2022-03-22 01:53:12.749 [INFO] Status: Downloaded newer image for harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount:0.0.3
100%|██████████| 3/3 [00:00<00:00,  9.69it/s]
2022-03-22 01:53:12.854 [INFO] Pull image successfully !
```

### tag images

tag images in container's host node.

```python
docker.tag_images(original_repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                  original_tag="0.0.3",
                  target_repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                  target_tag="0.0.3"
                 )

2022-03-22 02:03:55.017 [INFO] Tag repository successfully !

docker.show_images(grep="service.stonewise.cn")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount:0.0.3	d3838c66fc1e	2022-03-14T02:19:02.010	1.0 GB
```
### push images

push images to service.stonewise.cn:5000/ or harbor (recommend)

Similar to cmd line ``docker push xxx``

```python
docker.push_images(repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/793 [00:00<?, ?it/s]2022-03-23 06:52:54.661 [INFO] The push refers to repository [service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount]
  0%|          | 1/793 [00:00<01:20,  9.83it/s]2022-03-23 06:52:54.764 [INFO] Preparing
  0%|          | 2/793 [00:00<01:21,  9.76it/s]2022-03-23 06:52:54.867 [INFO] Waiting
  3%|▎         | 20/793 [00:00<00:09, 85.39it/s]2022-03-23 06:52:54.970 [INFO] Pushing
...
 96%|█████████▌| 758/793 [00:03<00:00, 368.36it/s]2022-03-23 06:52:57.730 [INFO] Pushed
2022-03-23 06:52:57.831 [INFO] 0.0.3: digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4 size: 4079
2022-03-23 06:52:57.933 [INFO] {}
100%|██████████| 793/793 [00:03<00:00, 235.06it/s]
2022-03-23 06:52:58.036 [INFO] Push image successfully !
```

### build images

build images for harbor or service.stonewise.cn:5000/

Similar to cmd line ``docker build -f Dockerfile -t xxx ./``

`tips:` use this fun in the same dir as Dockerfile, no extra file (or data file in the same dir)

```python
docker.build_images(path="/home/jovyan/image",
                    dockerfile="Dockerfile",
                    repository="service.stonewise.cn:5000/standalone-training",tag="0.0.1")

  0%|          | 0/14 [00:00<?, ?it/s]2022-03-23 07:35:22.763 [INFO] Step 1/3 : FROM harbor-qzm.stonewise.cn/proxy_cache/kubeflow/tensorflow:1.14.0-py3.6-cpu
  7%|▋         | 1/14 [00:00<00:01,  9.88it/s]2022-03-23 07:35:22.866 [INFO] 
...
 93%|█████████▎| 13/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:24.103 [INFO] Successfully tagged service.stonewise.cn:5000/standalone-training:0.0.1
100%|██████████| 14/14 [00:01<00:00,  9.70it/s]
2022-03-23 07:35:24.208 [INFO] Build image successfully !

docker.push_images(repository="service.stonewise.cn:5000/standalone-training", tag="0.0.1")

  0%|          | 0/525 [00:00<?, ?it/s]2022-03-23 07:37:37.084 [INFO] The push refers to repository [service.stonewise.cn:5000/standalone-training]
  0%|          | 1/525 [00:00<00:53,  9.88it/s]2022-03-23 07:37:37.186 [INFO] Preparing
  0%|          | 2/525 [00:00<00:53,  9.81it/s]2022-03-23 07:37:37.289 [INFO] Waiting
  2%|▏         | 11/525 [00:00<00:11, 45.49it/s]2022-03-23 07:37:37.392 [INFO] Pushing
...
100%|█████████▉| 523/525 [00:01<00:00, 854.64it/s]2022-03-23 07:37:38.620 [INFO] 0.0.1: digest: sha256:0fe6eaa12c2e4409f2b20f089dca83e8f0b4480b60405dcbb102a00185b2070c size: 2215
2022-03-23 07:37:38.721 [INFO] {}
100%|██████████| 525/525 [00:01<00:00, 301.85it/s]
2022-03-23 07:37:38.825 [INFO] Push image successfully !
```

### commit containers

commit containers to images in  harbor or service.stonewise.cn:5000/

Similar to cmd line ``docker commit <container_id> xxx``

if `push_image=True` committed image will be pushed

`tips`: before committing, you can use `show_containers()` to get your container id 

```python
docker.show_containers()

CONTAINER ID	CREATED	STATUS	PORTS	IMAGE	COMMAND	CONTAINER NAME
e96742819503	2022-04-06 10:53:12	Up 3 minutes		harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-image@sha256:1deea8bc1e94c2ee7e63c146cdfe6ffa6cf46e99c7c64aeb8a75bf2d5293840c	/entrypoint.sh /bin/bash /usr/src/app/startup.sh	k8s_base_base-0_liuweibin_554565fb-659a-4a06-b2e8-f188bd5c38ed_0
```

```python
docker.commit_containers(
    container="e96742819503",
    repository="service.stonewise.cn:5000/notebook-server",
    tag="base",
    push_image=True
)

2022-04-06 10:58:31.417 [INFO] Commit container sucessfully !
  0%|          | 0/5561 [00:00<?, ?it/s]2022-04-06 11:02:32.232 [INFO] The push refers to repository [service.stonewise.cn:5000/notebook-server]
  0%|          | 1/5561 [00:00<09:24,  9.86it/s]2022-04-06 11:02:32.336 [INFO] Preparing
  0%|          | 2/5561 [00:00<09:28,  9.77it/s]2022-04-06 11:02:32.438 [INFO] Waiting
  0%|          | 23/5561 [00:00<00:56, 98.81it/s]2022-04-06 11:02:32.541 [INFO] Preparing
...
 94%|█████████▎| 5201/5561 [00:07<00:00, 2452.10it/s]2022-04-06 11:02:40.109 [INFO] Pushing
2022-04-06 11:02:40.210 [INFO] Pushed
2022-04-06 11:02:40.312 [INFO] Pushing
2022-04-06 11:02:40.414 [INFO] Pushed
2022-04-06 11:02:40.516 [INFO] base: digest: sha256:60ae6bf7977b719155119ae9eb0e36605227bb867a97b612a4d3f437e3bf9410 size: 7864
2022-04-06 11:02:40.618 [INFO] {}
100%|██████████| 5561/5561 [00:08<00:00, 655.23it/s] 
2022-04-06 11:02:40.725 [INFO] Push image successfully !
```