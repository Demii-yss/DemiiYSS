const ROOT_URL = window.location.pathname

async function makeRequest(url, method, body){
    let headers = new Headers()
    headers.append('X-Requested-With', 'XMLHttpRequest')
    headers.append('Content-Type', 'application/json')

    let init = {
        method: method,
        headers: headers,
        body: body
    }

    if (method === 'post'){
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        headers.append('X-CSRFToken', csrf)
    }

    let res = await fetch(url, init)
    return await res.json()
}

async function generate_gif(original_image_files){
    let static_folder = JSON.parse(document.getElementById('static_folder').textContent)
    if (document.getElementById('gif_display') != null) {
        document.getElementById('gif_display').remove()
    }
    let image_order = []
    document.querySelectorAll('.uploadImageList').forEach(function (elm, idx){
                image_order.push(elm.getAttribute('data-original-order'))
            })
    let image_duration = []
    document.querySelectorAll('.timeRange').forEach(function (elm, idx){
                image_duration.push(elm.value)
            })
    console.log(static_folder)

    let data = await makeRequest(
        url = ROOT_URL,
        method='post',
        content=JSON.stringify({
            mode: 'generate_gif',
            image_order: image_order,
            image_duration: image_duration,
            images: original_image_files,
            static_folder: static_folder
        }))

    let gif_div = document.createElement('div')
    gif_div.id = 'gif_display'
    gif_div.classList.add("container-lg")
    gif_div.classList.add("my-5")

    let gif_img = document.createElement('img')
    gif_img.id = 'gif_img'
    gif_img.src = '/' + data['gif_path']
    gif_img.style = 'object-fit: contain height: 40%; width: 40%;'
    gif_div.appendChild(gif_img)
    document.body.appendChild(gif_div)
    return data['gif_path']
}


function initDragAndDropList(){
    const sortableList = document.querySelector('.sortable-list')
    const uploadImageItems = sortableList.querySelectorAll('.uploadImageList')

    uploadImageItems.forEach(item => {
        item.addEventListener("dragstart", () => {
            setTimeout(() => item.classList.add("dragging"), 0)
        })
        item.addEventListener("dragend", () => {
            item.classList.remove("dragging");
            sortableList.querySelectorAll('.uploadImageList').forEach(function (elm, idx){
                elm.setAttribute('data-final-order', (idx+1).toString())
                elm.querySelector('.image-order').innerHTML = (idx+1).toString()
            })
        })
    })

    const initSortableList = (e) => {
        e.preventDefault();
        const draggingItem = sortableList.querySelector('.dragging')
        const siblings = [...sortableList.querySelectorAll(".uploadImageList:not(.dragging)")]
        let nextSibling = siblings.find(sibling => {
            return e.clientY <= sibling.getBoundingClientRect().top + sibling.offsetHeight/2
        })

        sortableList.insertBefore(draggingItem, nextSibling)
    }

    sortableList.addEventListener("dragover", initSortableList)
}

function initSlider(){
    const sliders = document.querySelectorAll('.timeRange')
    for (const key of Object.keys(sliders)) {
        sliders[key].oninput = function() {
            document.querySelector('#label' + this.id).innerHTML = this.value + 's'
        }
    }
    document.getElementById('timeRangeAll').oninput = function() {
        for (const key of Object.keys(sliders)) {
            sliders[key].value = this.value
            document.querySelector('#label' + sliders[key].id).innerHTML = this.value + 's'
        }
    }
}


async function leaveSite(){
    let static_folder = JSON.parse(document.getElementById('static_folder').textContent)
    let data = await makeRequest(
        url = ROOT_URL,
        method='post',
        content=JSON.stringify({
            mode: 'leave_site',
            static_folder: static_folder
        }))
}

async function bodyLoaded(){
    initSlider()
    initDragAndDropList()
    window.onunload = function(){
        alert('?')
        leaveSite()
    };
}

