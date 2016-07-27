watch -n 20 " find . -name \"*.log\" -cmin -1 -type f -exec ./moncmd.sh {} \; "
