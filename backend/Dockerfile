# Smart Resume Analyzer Backend - Dockerfile
FROM openjdk:17-jdk-alpine
WORKDIR /app
ARG JAR_FILE=target/smart-resume-analyzer-backend-1.0.0.jar
COPY ${JAR_FILE} /app/app.jar
RUN mkdir -p /app/data /app/logs
EXPOSE 8080
ENV SRA_DB_PATH=/app/data/smart_resume_analyzer.db OPENAI_API_KEY="" JAVA_OPTS=""
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD nc -z localhost 8080 || exit 1
ENTRYPOINT ["sh","-c","java $JAVA_OPTS -jar /app/app.jar"]
