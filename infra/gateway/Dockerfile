FROM nginx:1.25.4-alpine

EXPOSE 80

COPY nginx.conf /etc/nginx/templates/default.conf.template

# start nginx in foreground to not have container killed immediately
CMD ["nginx", "-g", "daemon off;"]