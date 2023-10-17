#!/bin/bash
thera -s css
thera mypage.md -t templates/main.html
thera blog/*.md -t templates/blog.html -b templates/blog-index.html
