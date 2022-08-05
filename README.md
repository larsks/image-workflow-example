## Overview

This repository demonstrates how to automate Docker image building and tagging how to coordinate image releases with Kubernetes manifests contained in the same repository.

Docker images are built using a GitHub workflow defined in [`.github/workflows/build-image.yaml`](.github/workflows/build-image.yaml). We use the action `docker/metadata-action` to extract metadata from the image in order to generate image tags:

```
      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern=v{{version}}
            type=semver,pattern=v{{major}}.{{minor}}
            type=semver,pattern=v{{major}}
            type=ref,event=branch
            type=sha
```

For every push to the repository, this will build an image and tag it with:

- The branch name
- The commit hash

For every tag we create using a [semantic-version][semver] version number (`<major>.<minor>.<patch>`), we tag the image with:

- The version number (`v1.2.3`)
- The minor version (`v1.2`)
- The major version (`v1`)

This allows consumers to pin their images to a specific version (`someimage:v1.2.3`) or just to the major version (`someimage:v1`), allowing them to take advantage of non-breaking updates.

[semver]: https://semver.org/

## Deploying the manifests

The manifests included in this repository can be deployed using the [Kustomize][] functionality build into recent versions of `kubectl`.

[kustomize]: https://kustomize.io/

### In OpenShift

```
kubectl apply -k k8s/overlays/with-route
```

### In Kubernetes

You will need to edit `k8s/overlays/with-ingress/ingress.yaml` to change the hostname to something resolvable in your local environment.

```
kubectl apply -k k8s/overlays/with-ingress
```

## Cleaning up

To clean up a deployment, replace `apply` with `delete` in the above examples:

```
kubectl delete -k k8s/overlays/with-route
```

## Viewing manifests

This repository relies on the [Kustomize][] support built into `kubectl` to generate manifests. If you just want to see the generated manifests without deploying them, install [Kustomize][] and then run e.g:

```
kustomize build k8s/overlays/with-route | less
```

[kustomize]: https://kustomize.io/

## Contributing

We'd love to have you contribute! Please refer to our [contribution
guidelines](CONTRIBUTING.md) for details.

## License

[Apache 2.0 License](LICENSE).

The code is provided as-is with no warranties.
