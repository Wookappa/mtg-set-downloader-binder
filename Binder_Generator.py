import os
import re


def contains_number(string):
    return bool(re.search(r'\d', string))


def select_image_folder():
    print("Select an image folder:")
    folders = [folder for folder in os.listdir("art/") if folder != ".DS_Store"]
    for i, folder in enumerate(folders):
        print(f"{i + 1}. {folder}")

    selection = int(input("Enter the folder number: ")) - 1
    if 0 <= selection < len(folders):
        return os.path.join("art/", folders[selection])
    else:
        return None


def generate_image_gallery(images, grid_size=(8, 4), images_per_page=32, folder_name="Binder"):
    num_images = len(images)
    grid_rows, grid_cols = grid_size
    num_pages = (num_images - 1) // images_per_page + 1

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <style>
            .gallery-container {
                display: grid;
                grid-template-columns: repeat({grid_cols}, 1fr);
                grid-gap: 10px;
                justify-content: center;
                align-items: center;
                margin: 0 auto;
            }

            .gallery-item {
                position: relative;
                width: 100%;
                height: 100%;
            }

            .gallery-item img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
                cursor: pointer;
                transition: transform 0.2s;
            }

            .gallery-item img:hover {
                transform: scale(1.1);
            }

            .gallery-preview {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: none;
                justify-content: center;
                align-items: center;
                background-color: rgba(0, 0, 0, 0.9);
                z-index: 999;
            }

            .gallery-preview img {
                max-width: 90%;
                max-height: 90%;
                object-fit: contain;
            }

            .close {
                position: absolute;
                top: 15px;
                right: 35px;
                color: #f1f1f1;
                font-size: 40px;
                font-weight: bold;
                transition: 0.3s;
                cursor: pointer;
            }

            .close:hover,
            .close:focus {
                color: #bbb;
                text-decoration: none;
                cursor: pointer;
            }

            .pagination {
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }

            .pagination a {
                margin: 0 5px;
                cursor: pointer;
                text-decoration: none;
            }

            .pagination a.active {
                font-weight: bold;
            }         
        </style>
        <script>
            var galleryPages;
            var currentPage;

            function showPage(pageIndex) {
                var paginationLinks = document.getElementsByClassName('pagination-link');

                currentPage = pageIndex;

                for (var i = 0; i < galleryPages.length; i++) {
                    if (i === pageIndex) {
                        galleryPages[i].style.display = 'grid';
                        paginationLinks[i + 1].classList.add('active');
                    } else {
                        galleryPages[i].style.display = 'none';
                        paginationLinks[i + 1].classList.remove('active');
                    }
                }
            }

            function showPreviousPage(maxPages) {
                if (currentPage > 0) {
                    currentPage -= 1;
                    showPage(currentPage);
                    hideIfMoreThanMax(currentPage, maxPages);
                }
            }
            
            function showNextPage(maxPages) {
                if (currentPage < galleryPages.length - 1) {
                    currentPage += 1;
                    showPage(currentPage);
                    hideIfMoreThanMax(currentPage, maxPages);
                }
            }

            function showImagePreview(imageSrc) {
                var previewContainer = document.getElementById('image-preview-container');
                var previewImage = document.getElementById('image-preview');
                previewImage.src = imageSrc;
                previewContainer.style.display = 'flex';
            }

            function hideImagePreview() {
                var previewContainer = document.getElementById('image-preview-container');
                previewContainer.style.display = 'none';
            }

            function hideIfMoreThanMax(page, maxPages) {
                var hiddenPages = document.getElementsByClassName('hidden-page');
                var firstVisiblePage 
                var lastVisiblePage

                for (var i = 0; i < hiddenPages.length; i++) {
                    if (hiddenPages[i].style.display === "block") {
                        if (!firstVisiblePage) {
                            firstVisiblePage = hiddenPages[i];
                        }
                        lastVisiblePage = hiddenPages[i];
                    }
                }

                var spanPages = 5;
                var startPage = parseInt(firstVisiblePage.textContent, 10);
                var endPage = parseInt(lastVisiblePage.textContent, 10);
                var acceptableDiff = (endPage - startPage) == maxPages
                console.log(acceptableDiff, endPage - startPage)


                spanPagesStart = startPage > 1 ? startPage - 1 : spanPages;
                spanPagesEnd = hiddenPages.length - endPage >= spanPages ? spanPages : hiddenPages.length - endPage
                
                console.log("pagtot ",hiddenPages.length)
                console.log("startPage ",startPage)
                console.log("endPage ",endPage)
                console.log("spanPages ",spanPages)
                console.log("page + spanPages ",page + spanPages)
                
                if (page + spanPagesEnd >= endPage) {
                    startPage += spanPagesEnd
                    endPage += spanPagesEnd
                }else if ((page < startPage + spanPagesStart) && (page > spanPagesStart)) {
                    endPage -= spanPagesStart;
                    startPage -= spanPagesStart;
                }

                for (var i = 0; i < hiddenPages.length; i++) {
                    if (i + 1 >= startPage && i < endPage) {
                        hiddenPages[i].style.display = "block";
                    } else {
                        hiddenPages[i].style.display = "none";
                    }
                }
            }
        </script>
    </head>
    <body>
    """

    for page in range(num_pages):
        start_idx = page * images_per_page
        end_idx = min(start_idx + images_per_page, num_images)
        image_subset = images[start_idx:end_idx]

        html += f'<div class="gallery-page" style="display: {"grid" if page == 0 else "none"};">'
        html += f'<div class="gallery-container" style="display: grid; grid-template-columns: repeat({grid_rows}, 1fr);">'

        for image_path in image_subset:
            image_filename = os.path.basename(image_path)
            html += f'<div class="gallery-item"><img src="{os.path.abspath(image_path)}" onclick="showImagePreview(this.src)"></div>'
            # html += f'<div class="gallery-item"><img src="{os.path.abspath(image_path)}" onclick="showImagePreview(this.src)" style="max-width: 200px; max-height: 200px;"></div>'

        html += "</div>"
        html += "</div>"

    html += "<div class='pagination'>"

    max_pages = 40
    html += f'<a class="pagination-link" onclick="showPreviousPage({max_pages})">Previous</a>'
    for page in range(num_pages):
        # html += f'<a class="pagination-link" onclick="hideIfMoreThanMax(max_pages); showPage({page})">{page + 1}</a>'
        html += f'<a class="pagination-link hidden-page" onclick="hideIfMoreThanMax({page}, {max_pages}); showPage({page})">{page + 1}</a>'
    html += f'<a class="pagination-link" onclick="showNextPage({max_pages})">Next</a>'

    html += "</div>"

    html += """
    <div id="image-preview-container" class="gallery-preview" onclick="hideImagePreview()">
        <span class="close" onclick="closeModal()">&times;</span>
        <img id="image-preview" src="">
    </div>

    <script>
        galleryPages = document.getElementsByClassName('gallery-page');
        showPage(0);
        var hiddenPages = document.getElementsByClassName('hidden-page');   
        var maxPages = """ + str(max_pages) + """;
        for (var i = 0; i < hiddenPages.length; i++) {
            if (i > maxPages) {
              hiddenPages[i].style.display = "none";
            } else {
              hiddenPages[i].style.display = "block";
            }
        }
    </script>
    </body>
    </html>
    """
    file_name = folder_name + "_Binder.html"
    with open(file_name, "w") as f:
        f.write(html)


# Select image folder
image_folder = select_image_folder()

if image_folder:
    # Read all image files from the selected folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   os.path.isfile(os.path.join(image_folder, f))]
    image_files = list(filter(contains_number, image_files))

    # Sort images based on the number in the file name
    image_files.sort(key=lambda x: int(re.findall(r"\d+", x)[-1]))

    # Grid size
    grid_cols = int(input("Enter the number of grid columns: "))
    grid_rows = int(input("Enter the number of grid rows: "))

    # Generate image gallery in a web page with 8x4 grid and pagination
    generate_image_gallery(image_files, grid_size=(grid_cols, grid_rows), images_per_page=grid_cols * grid_rows,
                           folder_name=os.path.basename(image_folder))
