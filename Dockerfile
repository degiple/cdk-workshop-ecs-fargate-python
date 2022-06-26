FROM gitpod/workspace-python

COPY ./completion.bash ./

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip && sudo ./aws/install && rm awscliv2.zip 

RUN sudo apt -y install nodejs npm --no-install-recommends \
    && sudo npm install -g n && sudo n stable && sudo apt purge -y nodejs npm \
    && sudo npm install -g aws-cdk && bash completion.bash
