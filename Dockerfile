FROM gitpod/workspace-python

# Install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip && sudo ./aws/install && rm awscliv2.zip 

# Install aws cdk cli
RUN sudo apt -y install nodejs npm --no-install-recommends \
    && sudo npm install -g n && sudo n stable && sudo apt purge -y nodejs npm \
    && sudo npm update -g npm && sudo npm install -g aws-cdk

# Enabled tab completion
COPY ./completion.bash ./
RUN cat completion.bash >> /home/gitpod/.bashrc
