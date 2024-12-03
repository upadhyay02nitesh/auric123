FROM python:3.10

# Install system dependencies, Rust toolchain, and build essentials
RUN apt-get update && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && echo 'source $HOME/.cargo/env' >> /etc/profile.d/cargo.sh \
    && . $HOME/.cargo/env \
    && export PATH="$HOME/.cargo/bin:$PATH"

# Set working directory
WORKDIR /shoppinglyx

# Copy project files
COPY . .

# Upgrade pip and install dependencies
RUN . $HOME/.cargo/env && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run migrations, collect static files, and start the server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
