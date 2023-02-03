cupcake_list = document.querySelector('.cupcakes-board')
form = document.querySelector('.add-cupcake-form')

async function getCupcakes() {
    response = await axios.get("/api/cupcakes")
    console.log(response["data"]["cupcakes"])
    for (let cupcake of response["data"]["cupcakes"]) {
        createCupcakeCard(cupcake)

        console.log(cupcake)
    }
}

function createCupcakeCard(data) {
    let new_cupcake = document.createElement('div')
    let title = document.createElement('h3')
    let cupcake_info = document.createElement('p')
    let cupcake_img = document.createElement('img')
    new_cupcake.classList.add('cupcake-card')
    title.textContent = data["flavor"]
    cupcake_info.textContent = `Size: ${data["size"]}, Rating: ${data['rating']}/10`
    cupcake_info.classList.add('cupcake-info')
    cupcake_img.setAttribute('src', data['image'])
    cupcake_img.classList.add('card-image')
    new_cupcake.append(title)
    new_cupcake.append(cupcake_info)
    new_cupcake.append(cupcake_img)
    cupcake_list.append(new_cupcake)
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    default_img = "https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg"
    let flavor = document.querySelector('#flavor');
    let size = document.querySelector('#size');
    let rating = document.querySelector('#rating');
    let img = document.querySelector('#image_url');
    let img_url = img.value ? img.value : default_img;
    data = {
        "flavor": flavor.value,
        "size": size.value,
        "rating": rating.value,
        "image": img_url
    };
    url = '/api/cupcakes';
    response = await axios.post(url, json = data);
    createCupcakeCard(response['data']['cupcake']);
    flavor.value = '';
    rating.value = '';
    img.value = '';
})
getCupcakes()