# React + Bun + Kubernetes Boilerplate

This project is a modern, production-ready boilerplate for building and deploying a React frontend application. It features a lightning-fast development environment with Bun, a highly optimized containerization workflow with Docker/Podman, and a scalable deployment strategy using Kubernetes and Helm.

![Screenshot of the application UI](./preview.png)

## Core Concepts

This boilerplate is built on a set of modern, high-performance tools chosen to create a streamlined and efficient workflow.

| Stage       | Tool                  | Why                                          |
| ----------- | --------------------- | -------------------------------------------- |
| Dev/Build   | **Bun**               | No npm, fast TypeScript-native builds        |
| Packaging   | **Docker (multi-stage)** | Compact final image (~20MB)                  |
| Deployment  | **Helm + Kubernetes** | Declarative, scalable, and cloud-native      |
| Runtime     | **NGINX**             | Serve static React build, not a Node server  |

## Features

- **Frontend:** React 18 with TypeScript and a beautiful UI built with Tailwind CSS.
- **Development:** Extremely fast development, testing, and package management powered by Bun.
- **Containerization:** Optimized, multi-stage `Dockerfile` for small, secure production images. Compatible with both Docker and Podman.
- **Deployment:** Declarative deployments to any Kubernetes cluster using a production-ready Helm chart.
- **Code Quality:** Well-structured and refactored code with a component-based architecture.

## Prerequisites

Before you begin, ensure you have the following tools installed on your system:

- **Bun:** For local development and package management.
- **Podman** or **Docker:** For building and pushing container images.
- **kubectl:** For interacting with your Kubernetes cluster.
- **Helm:** For managing Kubernetes deployments.
- **make:** For easily running the commands defined in the `Makefile`.

## Getting Started

There are two primary ways to run this application: locally for development or deployed to a Kubernetes cluster.

### Local Development

For local development, you can run the application with hot-reloading using Bun's built-in development server.

1.  **Install Dependencies:**
    ```bash
    bun install
    ```

2.  **Start the Development Server:**
    ```bash
    bun run dev
    ```

The application will be available at `http://localhost:5173`.

### Kubernetes Deployment

To deploy the application to a Kubernetes cluster, you will need access to a container registry (like Docker Hub, GHCR, etc.) that your cluster can pull images from.

1.  **Configure the Registry in `values.yaml`:**
    Open `charts/frontend/values.yaml` and update the `image.repository` to point to your container registry and repository.

2.  **Build and Push the Image:**
    Use the `make` commands to build and push your image. You will need to be logged into your container registry (`podman login your-registry.io`).

    ```bash
    # Build the container image
    make podman-build

    # Tag the image with your repository and a version
    podman tag localhost/react-bun-k8s:latest your-registry.io/your-repo:latest

    # Push the image
    podman push your-registry.io/your-repo:latest
    ```

3.  **Deploy with Helm:**
    Use the `helm-upgrade` command from the `Makefile`. This will install or upgrade the release in the `web` namespace, creating it if it doesn't exist.

    ```bash
    make helm-upgrade
    ```

    If your repository is private, make sure you have created an `imagePullSecrets` in the `web` namespace and configured it in the `values.yaml` file.

## Makefile Commands

This project includes a `Makefile` with convenient shortcuts for common tasks.

- `make podman-build`: Builds the container image using Podman.
- `make podman-push IMAGE=...`: Pushes a specified image to a registry.
- `make helm-install`: Installs the Helm chart.
- `make helm-upgrade`: Upgrades the Helm release.
- `make helm-uninstall`: Uninstalls the Helm release.
- `make dev`: Starts the local development server.
- `make build`: Builds the production version of the application.

## Project Structure

- **`.github/workflows/`**: Contains the CI/CD pipeline for automated deployments.
- **`charts/frontend/`**: The Helm chart for deploying the application to Kubernetes.
- **`public/`**: Static assets and the main `index.html` file.
- **`src/`**: The React application source code.
  - **`components/`**: Reusable React components.
- **`Dockerfile`**: Multi-stage Dockerfile for building the production image.
- **`nginx.conf`**: Custom Nginx configuration for serving the React application.
- **`Makefile`**: A set of shortcuts for common development and deployment tasks.

## Future Improvements

- **Server-Side Rendering (SSR):** Extend the project to use SSR with Bun for improved performance and SEO.
- **GitOps:** Integrate with ArgoCD or FluxCD for a fully automated, GitOps-based deployment workflow.
- **Alternative Web Server:** Swap NGINX for Caddy for automatic HTTPS and a simpler configuration experience.