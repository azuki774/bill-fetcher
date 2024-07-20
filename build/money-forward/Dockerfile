FROM ghcr.io/azuki774/selenium-chrome:0.2.0

# Required Packages
RUN apt-get update && \
    apt-get install -y curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# AWS Setup
RUN curl -o /var/tmp/awscli.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip && \
    unzip -d /usr/local/bin/ /var/tmp/awscli.zip

COPY requirements/ /tmp/
RUN pip install --upgrade pip && pip install -r /tmp/moneyforward_requirements.txt
COPY --chmod=755 build/money-forward/main.sh /src/main.sh
COPY src/moneyforward/ /src/

ENTRYPOINT ["/src/main.sh"]
