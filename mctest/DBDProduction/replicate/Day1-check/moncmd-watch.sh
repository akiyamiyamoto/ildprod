
# watch -n 20 " find . -name \"*.replist\" -cmin -3 -type f -exec ./moncmd.sh {} \; "
watch -n 20 " find . -name \"*retry-rep.log\" -cmin -3 -type f -exec ./moncmd.sh {} \; "
