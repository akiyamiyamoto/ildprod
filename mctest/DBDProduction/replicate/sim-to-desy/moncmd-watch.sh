watch -n 20 " find . -name \"*.log\" -cmin -3 -type f -exec ./moncmd.sh {} \; "
