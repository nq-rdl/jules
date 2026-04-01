FROM node:20

ARG TZ
ENV TZ="$TZ"

ARG CLAUDE_CODE_VERSION=latest

# Install basic development tools and iptables/ipset
RUN apt-get update && apt-get install -y --no-install-recommends \
    less \
    git \
    procps \
    sudo \
    fzf \
    zsh \
    man-db \
    unzip \
    gnupg2 \
    gh \
    iptables \
    ipset \
    iproute2 \
    dnsutils \
    aggregate \
    jq \
    nano \
    vim \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Go (for Go-based skills: pi, jules, charm-tui, copilot-sdk, pdf-sr-extract)
ARG GO_VERSION=1.24.2
RUN ARCH=$(dpkg --print-architecture) && \
    curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-${ARCH}.tar.gz" | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:${PATH}"

# Install changie (changelog management)
ARG CHANGIE_VERSION=1.22.0
RUN ARCH=$(dpkg --print-architecture) && \
    curl -fsSL "https://github.com/miniscruff/changie/releases/download/v${CHANGIE_VERSION}/changie_${CHANGIE_VERSION}_linux_${ARCH}.tar.gz" | tar -C /usr/local/bin -xzf - changie

# Create non-root user
ARG USERNAME=dev
RUN useradd -m -s /bin/zsh ${USERNAME} && \
    mkdir -p /usr/local/share/npm-global && \
    chown -R ${USERNAME}:${USERNAME} /usr/local/share/npm-global

# Persist bash history
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory

ENV DEVCONTAINER=true

# Create workspace and config directories
RUN mkdir -p /workspace /home/${USERNAME}/.claude /home/${USERNAME}/go && \
    chown -R ${USERNAME}:${USERNAME} /workspace /home/${USERNAME}/.claude /home/${USERNAME}/go

WORKDIR /workspace

# Install git-delta
ARG GIT_DELTA_VERSION=0.18.2
RUN ARCH=$(dpkg --print-architecture) && \
    wget -q "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    dpkg -i "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    rm "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"

# Switch to non-root user
USER ${USERNAME}

# Set up npm global path
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH="${PATH}:/usr/local/share/npm-global/bin:/home/${USERNAME}/go/bin"
ENV GOPATH="/home/${USERNAME}/go"

ENV SHELL=/bin/zsh
ENV EDITOR=nano
ENV VISUAL=nano

# Install zsh with powerlevel10k
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git \
    -p fzf \
    -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
    -a "source /usr/share/doc/fzf/examples/completion.zsh" \
    -a "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    -x

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}

# Install pixi (conda-based package manager)
RUN curl -fsSL https://pixi.sh/install.sh | bash

# Copy and set up firewall script
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
    echo "${USERNAME} ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/${USERNAME}-firewall && \
    chmod 0440 /etc/sudoers.d/${USERNAME}-firewall

USER ${USERNAME}
