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

	const addressAutoComp = {
		url: autocompUrl,
		getValue: "address",
		template: {
			type: "description",
			fields:{
				description: "site_name"
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
$("#form-site-address").easyAutocomplete(addressAutoComp);
}) // closing ajax call


