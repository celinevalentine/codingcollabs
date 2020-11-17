function showRecipeCard(recipe, data, favorites) {
	const recipeHTML = generateRecipeCardHTML(recipe, data, favorites);
	$('#recipe-container').append(recipeHTML);
	$('form').on('submit', (e) => {
		e.preventDefault();
	});
}

function updateListContainer() {
	$('#list-container')
		.empty()
		.html(
			`<p class="text-center lead">Your list is empty!</p> <br> <a class="btn btn-outline-primary" href="/favorites">View Favorites</a>`
		);
}

function generateRecipeCardHTML(recipe, data, favorites) {
	let favButton;

	if (favorites.includes(recipe.id)) {
		favButton = `<button id="${recipe.id}" data-id="${recipe.id}" class='btn btn-sm'><span><i  class="fas fa-heart"></i></span></button>`;
	} else {
		favButton = `<button id="${recipe.id}" data-id="${recipe.id}" class='btn btn-sm'><span><i class="far fa-heart"></i></span></button>`;
	}

	return `<div class="card border mb-4 mx-auto p-2 rounded text-center">
	<a href="/recipes/${recipe.id}" class="card-link">
	<img src="${data.baseUri}${recipe.image}" class="card-img-top img-fluid" alt="Photo of ${recipe.title}">
	<div class="card-body py-2">
	  <h5 class="card-title d-inline">${recipe.title}</h5>
	  <form id="favorite-form" class="favorite-form d-inline">
		${favButton}
	  </form>
	  <p class="lead mb-0">Ready In: ${recipe.readyInMinutes} minutes</p>
	  <p class="lead">Servings: ${recipe.servings}</p>
	  <a class="small text-muted" href="${recipe.sourceUrl}">View original</a>
	  <br>
	  </a>
	</div>
</div>`;
}
function toggleFavorite(response) {
	if (response.status !== 200) {
		displayErrorAlert(response);
	} else {
		$(this).toggleClass('fas fa-heart');
		$(this).toggleClass('far fa-heart');
		displaySuccessAlert(response);
	}
}

function displayErrorAlert(response) {
	console.log(`Error details: ${response.data.errors}`);
	$('.feedback').remove();
	const alertHTML = generateAlertHTML('Something went wrong, please try again', 'danger');
	$('main').prepend(alertHTML).alert();
	$('.feedback').hide().fadeIn('slow').delay(1000).fadeOut('slow');
}

function displaySuccessAlert(response) {
	$('.feedback').remove();
	const alertHTML = generateAlertHTML(response.data.message, 'success');
	$('main').prepend(alertHTML).alert();
	$('.feedback').hide().fadeIn('slow').delay(1000).fadeOut('slow');
}

