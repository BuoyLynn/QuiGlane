const autocompUrl = "/api/sites-autocomp"
$.get(autocompUrl, () => {

	const siteAutoComp = {
		url: autocompUrl,
		getValue: "site_name",
		template: {
			type: "description",
			fields:{
				description: "address"
			}
		},
		list:{
			maxNumberOfElements: 7,
			hideAnimation:{
				type: "normal",
				time: 500,				
			},
			match:{
				enabled: true
			}
		}

	};

$("#form-site-name").easyAutocomplete(siteAutoComp);
})



// const autocompUrl = "/api/sites-autocomp";
// $.get(autocompUrl, () =>{

// 	var options = {

// 		url: autocompUrl,

// 		getValue: "site_name",

// 		template: {
// 							type: "description",
// 							fields: {
// 							description: "address"
// 							}
// 						},

// 		list: {
// 				maxNumberOfElements: 9,
// 				hideAnimation:{
// 						type: "slide",
// 						time: 500,
// 						callback: function (){}
// 											},
// 				match: {
// 						enabled: true
// 					}	
// 		},

// 		theme: "plate-dark"

// 		onChooseEvent: function(){
// 			let selected = ${"#form-site-name"}.getSelectedItemData();
// 			location.replace(selected["site_name"]);

// 		}
// };
	
// 	$("#form-site-name").easyAutocomplete(options);

// }); // close AJAX get request


