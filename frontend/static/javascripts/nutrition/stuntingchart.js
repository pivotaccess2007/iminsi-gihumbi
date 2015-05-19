// This code is from http://github.com/ewheeler/growthchart
//
////////////////////////////////
// Data
////////////////////////////////

function prepStuntingData(conf) {
	
	
	lhfa_boys_0_to_5_meta = {};
	lhfa_boys_0_to_5_meta.lines =  conf.lhfa_all_0_to_5_meta.lines.slice();
	lhfa_boys_0_to_5_meta.title = "Height for Age, Boys";

	lhfa_girls_0_to_5_meta = {};
	lhfa_girls_0_to_5_meta.lines = conf.lhfa_all_0_to_5_meta.lines.slice();
	lhfa_girls_0_to_5_meta.title = "Height for Age, Girls";

	lhfa_boys_0_to_5_zscores = [{
		"Month":"0",
		"L":"1",
		"M":"49.8842",
		"S":"0.03795",
		"SD":"1.8931",
		"SD3neg":"44.2",
		"SD2neg":"46.1",
		"SD1neg":"48",
		"SD0":"49.9",
		"SD1":"51.8",
		"SD2":"53.7",
		"SD3":"55.6"
	},
	{
		"Month":"1",
		"L":"1",
		"M":"54.7244",
		"S":"0.03557",
		"SD":"1.9465",
		"SD3neg":"48.9",
		"SD2neg":"50.8",
		"SD1neg":"52.8",
		"SD0":"54.7",
		"SD1":"56.7",
		"SD2":"58.6",
		"SD3":"60.6"
	},
	{
		"Month":"2",
		"L":"1",
		"M":"58.4249",
		"S":"0.03424",
		"SD":"2.0005",
		"SD3neg":"52.4",
		"SD2neg":"54.4",
		"SD1neg":"56.4",
		"SD0":"58.4",
		"SD1":"60.4",
		"SD2":"62.4",
		"SD3":"64.4"
	},
	{
		"Month":"3",
		"L":"1",
		"M":"61.4292",
		"S":"0.03328",
		"SD":"2.0444",
		"SD3neg":"55.3",
		"SD2neg":"57.3",
		"SD1neg":"59.4",
		"SD0":"61.4",
		"SD1":"63.5",
		"SD2":"65.5",
		"SD3":"67.6"
	},
	{
		"Month":"4",
		"L":"1",
		"M":"63.886",
		"S":"0.03257",
		"SD":"2.0808",
		"SD3neg":"57.6",
		"SD2neg":"59.7",
		"SD1neg":"61.8",
		"SD0":"63.9",
		"SD1":"66",
		"SD2":"68",
		"SD3":"70.1"
	},
	{
		"Month":"5",
		"L":"1",
		"M":"65.9026",
		"S":"0.03204",
		"SD":"2.1115",
		"SD3neg":"59.6",
		"SD2neg":"61.7",
		"SD1neg":"63.8",
		"SD0":"65.9",
		"SD1":"68",
		"SD2":"70.1",
		"SD3":"72.2"
	},
	{
		"Month":"6",
		"L":"1",
		"M":"67.6236",
		"S":"0.03165",
		"SD":"2.1403",
		"SD3neg":"61.2",
		"SD2neg":"63.3",
		"SD1neg":"65.5",
		"SD0":"67.6",
		"SD1":"69.8",
		"SD2":"71.9",
		"SD3":"74"
	},
	{
		"Month":"7",
		"L":"1",
		"M":"69.1645",
		"S":"0.03139",
		"SD":"2.1711",
		"SD3neg":"62.7",
		"SD2neg":"64.8",
		"SD1neg":"67",
		"SD0":"69.2",
		"SD1":"71.3",
		"SD2":"73.5",
		"SD3":"75.7"
	},
	{
		"Month":"8",
		"L":"1",
		"M":"70.5994",
		"S":"0.03124",
		"SD":"2.2055",
		"SD3neg":"64",
		"SD2neg":"66.2",
		"SD1neg":"68.4",
		"SD0":"70.6",
		"SD1":"72.8",
		"SD2":"75",
		"SD3":"77.2"
	},
	{
		"Month":"9",
		"L":"1",
		"M":"71.9687",
		"S":"0.03117",
		"SD":"2.2433",
		"SD3neg":"65.2",
		"SD2neg":"67.5",
		"SD1neg":"69.7",
		"SD0":"72",
		"SD1":"74.2",
		"SD2":"76.5",
		"SD3":"78.7"
	},
	{
		"Month":"10",
		"L":"1",
		"M":"73.2812",
		"S":"0.03118",
		"SD":"2.2849",
		"SD3neg":"66.4",
		"SD2neg":"68.7",
		"SD1neg":"71",
		"SD0":"73.3",
		"SD1":"75.6",
		"SD2":"77.9",
		"SD3":"80.1"
	},
	{
		"Month":"11",
		"L":"1",
		"M":"74.5388",
		"S":"0.03125",
		"SD":"2.3293",
		"SD3neg":"67.6",
		"SD2neg":"69.9",
		"SD1neg":"72.2",
		"SD0":"74.5",
		"SD1":"76.9",
		"SD2":"79.2",
		"SD3":"81.5"
	},
	{
		"Month":"12",
		"L":"1",
		"M":"75.7488",
		"S":"0.03137",
		"SD":"2.3762",
		"SD3neg":"68.6",
		"SD2neg":"71",
		"SD1neg":"73.4",
		"SD0":"75.7",
		"SD1":"78.1",
		"SD2":"80.5",
		"SD3":"82.9"
	},
	{
		"Month":"13",
		"L":"1",
		"M":"76.9186",
		"S":"0.03154",
		"SD":"2.426",
		"SD3neg":"69.6",
		"SD2neg":"72.1",
		"SD1neg":"74.5",
		"SD0":"76.9",
		"SD1":"79.3",
		"SD2":"81.8",
		"SD3":"84.2"
	},
	{
		"Month":"14",
		"L":"1",
		"M":"78.0497",
		"S":"0.03174",
		"SD":"2.4773",
		"SD3neg":"70.6",
		"SD2neg":"73.1",
		"SD1neg":"75.6",
		"SD0":"78",
		"SD1":"80.5",
		"SD2":"83",
		"SD3":"85.5"
	},
	{
		"Month":"15",
		"L":"1",
		"M":"79.1458",
		"S":"0.03197",
		"SD":"2.5303",
		"SD3neg":"71.6",
		"SD2neg":"74.1",
		"SD1neg":"76.6",
		"SD0":"79.1",
		"SD1":"81.7",
		"SD2":"84.2",
		"SD3":"86.7"
	},
	{
		"Month":"16",
		"L":"1",
		"M":"80.2113",
		"S":"0.03222",
		"SD":"2.5844",
		"SD3neg":"72.5",
		"SD2neg":"75",
		"SD1neg":"77.6",
		"SD0":"80.2",
		"SD1":"82.8",
		"SD2":"85.4",
		"SD3":"88"
	},
	{
		"Month":"17",
		"L":"1",
		"M":"81.2487",
		"S":"0.0325",
		"SD":"2.6406",
		"SD3neg":"73.3",
		"SD2neg":"76",
		"SD1neg":"78.6",
		"SD0":"81.2",
		"SD1":"83.9",
		"SD2":"86.5",
		"SD3":"89.2"
	},
	{
		"Month":"18",
		"L":"1",
		"M":"82.2587",
		"S":"0.03279",
		"SD":"2.6973",
		"SD3neg":"74.2",
		"SD2neg":"76.9",
		"SD1neg":"79.6",
		"SD0":"82.3",
		"SD1":"85",
		"SD2":"87.7",
		"SD3":"90.4"
	},
	{
		"Month":"19",
		"L":"1",
		"M":"83.2418",
		"S":"0.0331",
		"SD":"2.7553",
		"SD3neg":"75",
		"SD2neg":"77.7",
		"SD1neg":"80.5",
		"SD0":"83.2",
		"SD1":"86",
		"SD2":"88.8",
		"SD3":"91.5"
	},
	{
		"Month":"20",
		"L":"1",
		"M":"84.1996",
		"S":"0.03342",
		"SD":"2.814",
		"SD3neg":"75.8",
		"SD2neg":"78.6",
		"SD1neg":"81.4",
		"SD0":"84.2",
		"SD1":"87",
		"SD2":"89.8",
		"SD3":"92.6"
	},
	{
		"Month":"21",
		"L":"1",
		"M":"85.1348",
		"S":"0.03376",
		"SD":"2.8742",
		"SD3neg":"76.5",
		"SD2neg":"79.4",
		"SD1neg":"82.3",
		"SD0":"85.1",
		"SD1":"88",
		"SD2":"90.9",
		"SD3":"93.8"
	},
	{
		"Month":"22",
		"L":"1",
		"M":"86.0477",
		"S":"0.0341",
		"SD":"2.9342",
		"SD3neg":"77.2",
		"SD2neg":"80.2",
		"SD1neg":"83.1",
		"SD0":"86",
		"SD1":"89",
		"SD2":"91.9",
		"SD3":"94.9"
	},
	{
		"Month":"23",
		"L":"1",
		"M":"86.941",
		"S":"0.03445",
		"SD":"2.9951",
		"SD3neg":"78",
		"SD2neg":"81",
		"SD1neg":"83.9",
		"SD0":"86.9",
		"SD1":"89.9",
		"SD2":"92.9",
		"SD3":"95.9"
	},
	{
		"Month":"24",
		"L":"1",
		"M":"87.8161",
		"S":"0.03479",
		"SD":"3.0551",
		"SD3neg":"78.7",
		"SD2neg":"81.7",
		"SD1neg":"84.8",
		"SD0":"87.8",
		"SD1":"90.9",
		"SD2":"93.9",
		"SD3":"97"
	},
	{
		"Month":"24",
		"L":"1",
		"M":"87.1161",
		"S":"0.03507",
		"SD":"3.0551",
		"SD3neg":"78",
		"SD2neg":"81",
		"SD1neg":"84.1",
		"SD0":"87.1",
		"SD1":"90.2",
		"SD2":"93.2",
		"SD3":"96.3"
	},
	{
		"Month":"25",
		"L":"1",
		"M":"87.972",
		"S":"0.03542",
		"SD":"3.116",
		"SD3neg":"78.6",
		"SD2neg":"81.7",
		"SD1neg":"84.9",
		"SD0":"88",
		"SD1":"91.1",
		"SD2":"94.2",
		"SD3":"97.3"
	},
	{
		"Month":"26",
		"L":"1",
		"M":"88.8065",
		"S":"0.03576",
		"SD":"3.1757",
		"SD3neg":"79.3",
		"SD2neg":"82.5",
		"SD1neg":"85.6",
		"SD0":"88.8",
		"SD1":"92",
		"SD2":"95.2",
		"SD3":"98.3"
	},
	{
		"Month":"27",
		"L":"1",
		"M":"89.6197",
		"S":"0.0361",
		"SD":"3.2353",
		"SD3neg":"79.9",
		"SD2neg":"83.1",
		"SD1neg":"86.4",
		"SD0":"89.6",
		"SD1":"92.9",
		"SD2":"96.1",
		"SD3":"99.3"
	},
	{
		"Month":"28",
		"L":"1",
		"M":"90.412",
		"S":"0.03642",
		"SD":"3.2928",
		"SD3neg":"80.5",
		"SD2neg":"83.8",
		"SD1neg":"87.1",
		"SD0":"90.4",
		"SD1":"93.7",
		"SD2":"97",
		"SD3":"100.3"
	},
	{
		"Month":"29",
		"L":"1",
		"M":"91.1828",
		"S":"0.03674",
		"SD":"3.3501",
		"SD3neg":"81.1",
		"SD2neg":"84.5",
		"SD1neg":"87.8",
		"SD0":"91.2",
		"SD1":"94.5",
		"SD2":"97.9",
		"SD3":"101.2"
	},
	{
		"Month":"30",
		"L":"1",
		"M":"91.9327",
		"S":"0.03704",
		"SD":"3.4052",
		"SD3neg":"81.7",
		"SD2neg":"85.1",
		"SD1neg":"88.5",
		"SD0":"91.9",
		"SD1":"95.3",
		"SD2":"98.7",
		"SD3":"102.1"
	},
	{
		"Month":"31",
		"L":"1",
		"M":"92.6631",
		"S":"0.03733",
		"SD":"3.4591",
		"SD3neg":"82.3",
		"SD2neg":"85.7",
		"SD1neg":"89.2",
		"SD0":"92.7",
		"SD1":"96.1",
		"SD2":"99.6",
		"SD3":"103"
	},
	{
		"Month":"32",
		"L":"1",
		"M":"93.3753",
		"S":"0.03761",
		"SD":"3.5118",
		"SD3neg":"82.8",
		"SD2neg":"86.4",
		"SD1neg":"89.9",
		"SD0":"93.4",
		"SD1":"96.9",
		"SD2":"100.4",
		"SD3":"103.9"
	},
	{
		"Month":"33",
		"L":"1",
		"M":"94.0711",
		"S":"0.03787",
		"SD":"3.5625",
		"SD3neg":"83.4",
		"SD2neg":"86.9",
		"SD1neg":"90.5",
		"SD0":"94.1",
		"SD1":"97.6",
		"SD2":"101.2",
		"SD3":"104.8"
	},
	{
		"Month":"34",
		"L":"1",
		"M":"94.7532",
		"S":"0.03812",
		"SD":"3.612",
		"SD3neg":"83.9",
		"SD2neg":"87.5",
		"SD1neg":"91.1",
		"SD0":"94.8",
		"SD1":"98.4",
		"SD2":"102",
		"SD3":"105.6"
	},
	{
		"Month":"35",
		"L":"1",
		"M":"95.4236",
		"S":"0.03836",
		"SD":"3.6604",
		"SD3neg":"84.4",
		"SD2neg":"88.1",
		"SD1neg":"91.8",
		"SD0":"95.4",
		"SD1":"99.1",
		"SD2":"102.7",
		"SD3":"106.4"
	},
	{
		"Month":"36",
		"L":"1",
		"M":"96.0835",
		"S":"0.03858",
		"SD":"3.7069",
		"SD3neg":"85",
		"SD2neg":"88.7",
		"SD1neg":"92.4",
		"SD0":"96.1",
		"SD1":"99.8",
		"SD2":"103.5",
		"SD3":"107.2"
	},
	{
		"Month":"37",
		"L":"1",
		"M":"96.7337",
		"S":"0.03879",
		"SD":"3.7523",
		"SD3neg":"85.5",
		"SD2neg":"89.2",
		"SD1neg":"93",
		"SD0":"96.7",
		"SD1":"100.5",
		"SD2":"104.2",
		"SD3":"108"
	},
	{
		"Month":"38",
		"L":"1",
		"M":"97.3749",
		"S":"0.039",
		"SD":"3.7976",
		"SD3neg":"86",
		"SD2neg":"89.8",
		"SD1neg":"93.6",
		"SD0":"97.4",
		"SD1":"101.2",
		"SD2":"105",
		"SD3":"108.8"
	},
	{
		"Month":"39",
		"L":"1",
		"M":"98.0073",
		"S":"0.03919",
		"SD":"3.8409",
		"SD3neg":"86.5",
		"SD2neg":"90.3",
		"SD1neg":"94.2",
		"SD0":"98",
		"SD1":"101.8",
		"SD2":"105.7",
		"SD3":"109.5"
	},
	{
		"Month":"40",
		"L":"1",
		"M":"98.631",
		"S":"0.03937",
		"SD":"3.8831",
		"SD3neg":"87",
		"SD2neg":"90.9",
		"SD1neg":"94.7",
		"SD0":"98.6",
		"SD1":"102.5",
		"SD2":"106.4",
		"SD3":"110.3"
	},
	{
		"Month":"41",
		"L":"1",
		"M":"99.2459",
		"S":"0.03954",
		"SD":"3.9242",
		"SD3neg":"87.5",
		"SD2neg":"91.4",
		"SD1neg":"95.3",
		"SD0":"99.2",
		"SD1":"103.2",
		"SD2":"107.1",
		"SD3":"111"
	},
	{
		"Month":"42",
		"L":"1",
		"M":"99.8515",
		"S":"0.03971",
		"SD":"3.9651",
		"SD3neg":"88",
		"SD2neg":"91.9",
		"SD1neg":"95.9",
		"SD0":"99.9",
		"SD1":"103.8",
		"SD2":"107.8",
		"SD3":"111.7"
	},
	{
		"Month":"43",
		"L":"1",
		"M":"100.4485",
		"S":"0.03986",
		"SD":"4.0039",
		"SD3neg":"88.4",
		"SD2neg":"92.4",
		"SD1neg":"96.4",
		"SD0":"100.4",
		"SD1":"104.5",
		"SD2":"108.5",
		"SD3":"112.5"
	},
	{
		"Month":"44",
		"L":"1",
		"M":"101.0374",
		"S":"0.04002",
		"SD":"4.0435",
		"SD3neg":"88.9",
		"SD2neg":"93",
		"SD1neg":"97",
		"SD0":"101",
		"SD1":"105.1",
		"SD2":"109.1",
		"SD3":"113.2"
	},
	{
		"Month":"45",
		"L":"1",
		"M":"101.6186",
		"S":"0.04016",
		"SD":"4.081",
		"SD3neg":"89.4",
		"SD2neg":"93.5",
		"SD1neg":"97.5",
		"SD0":"101.6",
		"SD1":"105.7",
		"SD2":"109.8",
		"SD3":"113.9"
	},
	{
		"Month":"46",
		"L":"1",
		"M":"102.1933",
		"S":"0.04031",
		"SD":"4.1194",
		"SD3neg":"89.8",
		"SD2neg":"94",
		"SD1neg":"98.1",
		"SD0":"102.2",
		"SD1":"106.3",
		"SD2":"110.4",
		"SD3":"114.6"
	},
	{
		"Month":"47",
		"L":"1",
		"M":"102.7625",
		"S":"0.04045",
		"SD":"4.1567",
		"SD3neg":"90.3",
		"SD2neg":"94.4",
		"SD1neg":"98.6",
		"SD0":"102.8",
		"SD1":"106.9",
		"SD2":"111.1",
		"SD3":"115.2"
	},
	{
		"Month":"48",
		"L":"1",
		"M":"103.3273",
		"S":"0.04059",
		"SD":"4.1941",
		"SD3neg":"90.7",
		"SD2neg":"94.9",
		"SD1neg":"99.1",
		"SD0":"103.3",
		"SD1":"107.5",
		"SD2":"111.7",
		"SD3":"115.9"
	},
	{
		"Month":"49",
		"L":"1",
		"M":"103.8886",
		"S":"0.04073",
		"SD":"4.2314",
		"SD3neg":"91.2",
		"SD2neg":"95.4",
		"SD1neg":"99.7",
		"SD0":"103.9",
		"SD1":"108.1",
		"SD2":"112.4",
		"SD3":"116.6"
	},
	{
		"Month":"50",
		"L":"1",
		"M":"104.4473",
		"S":"0.04086",
		"SD":"4.2677",
		"SD3neg":"91.6",
		"SD2neg":"95.9",
		"SD1neg":"100.2",
		"SD0":"104.4",
		"SD1":"108.7",
		"SD2":"113",
		"SD3":"117.3"
	},
	{
		"Month":"51",
		"L":"1",
		"M":"105.0041",
		"S":"0.041",
		"SD":"4.3052",
		"SD3neg":"92.1",
		"SD2neg":"96.4",
		"SD1neg":"100.7",
		"SD0":"105",
		"SD1":"109.3",
		"SD2":"113.6",
		"SD3":"117.9"
	},
	{
		"Month":"52",
		"L":"1",
		"M":"105.5596",
		"S":"0.04113",
		"SD":"4.3417",
		"SD3neg":"92.5",
		"SD2neg":"96.9",
		"SD1neg":"101.2",
		"SD0":"105.6",
		"SD1":"109.9",
		"SD2":"114.2",
		"SD3":"118.6"
	},
	{
		"Month":"53",
		"L":"1",
		"M":"106.1138",
		"S":"0.04126",
		"SD":"4.3783",
		"SD3neg":"93",
		"SD2neg":"97.4",
		"SD1neg":"101.7",
		"SD0":"106.1",
		"SD1":"110.5",
		"SD2":"114.9",
		"SD3":"119.2"
	},
	{
		"Month":"54",
		"L":"1",
		"M":"106.6668",
		"S":"0.04139",
		"SD":"4.4149",
		"SD3neg":"93.4",
		"SD2neg":"97.8",
		"SD1neg":"102.3",
		"SD0":"106.7",
		"SD1":"111.1",
		"SD2":"115.5",
		"SD3":"119.9"
	},
	{
		"Month":"55",
		"L":"1",
		"M":"107.2188",
		"S":"0.04152",
		"SD":"4.4517",
		"SD3neg":"93.9",
		"SD2neg":"98.3",
		"SD1neg":"102.8",
		"SD0":"107.2",
		"SD1":"111.7",
		"SD2":"116.1",
		"SD3":"120.6"
	},
	{
		"Month":"56",
		"L":"1",
		"M":"107.7697",
		"S":"0.04165",
		"SD":"4.4886",
		"SD3neg":"94.3",
		"SD2neg":"98.8",
		"SD1neg":"103.3",
		"SD0":"107.8",
		"SD1":"112.3",
		"SD2":"116.7",
		"SD3":"121.2"
	},
	{
		"Month":"57",
		"L":"1",
		"M":"108.3198",
		"S":"0.04177",
		"SD":"4.5245",
		"SD3neg":"94.7",
		"SD2neg":"99.3",
		"SD1neg":"103.8",
		"SD0":"108.3",
		"SD1":"112.8",
		"SD2":"117.4",
		"SD3":"121.9"
	},
	{
		"Month":"58",
		"L":"1",
		"M":"108.8689",
		"S":"0.0419",
		"SD":"4.5616",
		"SD3neg":"95.2",
		"SD2neg":"99.7",
		"SD1neg":"104.3",
		"SD0":"108.9",
		"SD1":"113.4",
		"SD2":"118",
		"SD3":"122.6"
	},
	{
		"Month":"59",
		"L":"1",
		"M":"109.417",
		"S":"0.04202",
		"SD":"4.5977",
		"SD3neg":"95.6",
		"SD2neg":"100.2",
		"SD1neg":"104.8",
		"SD0":"109.4",
		"SD1":"114",
		"SD2":"118.6",
		"SD3":"123.2"
	},
	{
		"Month":"60",
		"L":"1",
		"M":"109.9638",
		"S":"0.04214",
		"SD":"4.6339",
		"SD3neg":"96.1",
		"SD2neg":"100.7",
		"SD1neg":"105.3",
		"SD0":"110",
		"SD1":"114.6",
		"SD2":"119.2",
		"SD3":"123.9"
	}
];

	lhfa_girls_0_to_5_zscores = [{
		"Month":"0",
		"L":"1",
		"M":"49.1477",
		"S":"0.0379",
		"SD":"1.8627",
		"SD3neg":"43.6",
		"SD2neg":"45.4",
		"SD1neg":"47.3",
		"SD0":"49.1",
		"SD1":"51",
		"SD2":"52.9",
		"SD3":"54.7"
	},
	{
		"Month":"1",
		"L":"1",
		"M":"53.6872",
		"S":"0.0364",
		"SD":"1.9542",
		"SD3neg":"47.8",
		"SD2neg":"49.8",
		"SD1neg":"51.7",
		"SD0":"53.7",
		"SD1":"55.6",
		"SD2":"57.6",
		"SD3":"59.5"
	},
	{
		"Month":"2",
		"L":"1",
		"M":"57.0673",
		"S":"0.03568",
		"SD":"2.0362",
		"SD3neg":"51",
		"SD2neg":"53",
		"SD1neg":"55",
		"SD0":"57.1",
		"SD1":"59.1",
		"SD2":"61.1",
		"SD3":"63.2"
	},
	{
		"Month":"3",
		"L":"1",
		"M":"59.8029",
		"S":"0.0352",
		"SD":"2.1051",
		"SD3neg":"53.5",
		"SD2neg":"55.6",
		"SD1neg":"57.7",
		"SD0":"59.8",
		"SD1":"61.9",
		"SD2":"64",
		"SD3":"66.1"
	},
	{
		"Month":"4",
		"L":"1",
		"M":"62.0899",
		"S":"0.03486",
		"SD":"2.1645",
		"SD3neg":"55.6",
		"SD2neg":"57.8",
		"SD1neg":"59.9",
		"SD0":"62.1",
		"SD1":"64.3",
		"SD2":"66.4",
		"SD3":"68.6"
	},
	{
		"Month":"5",
		"L":"1",
		"M":"64.0301",
		"S":"0.03463",
		"SD":"2.2174",
		"SD3neg":"57.4",
		"SD2neg":"59.6",
		"SD1neg":"61.8",
		"SD0":"64",
		"SD1":"66.2",
		"SD2":"68.5",
		"SD3":"70.7"
	},
	{
		"Month":"6",
		"L":"1",
		"M":"65.7311",
		"S":"0.03448",
		"SD":"2.2664",
		"SD3neg":"58.9",
		"SD2neg":"61.2",
		"SD1neg":"63.5",
		"SD0":"65.7",
		"SD1":"68",
		"SD2":"70.3",
		"SD3":"72.5"
	},
	{
		"Month":"7",
		"L":"1",
		"M":"67.2873",
		"S":"0.03441",
		"SD":"2.3154",
		"SD3neg":"60.3",
		"SD2neg":"62.7",
		"SD1neg":"65",
		"SD0":"67.3",
		"SD1":"69.6",
		"SD2":"71.9",
		"SD3":"74.2"
	},
	{
		"Month":"8",
		"L":"1",
		"M":"68.7498",
		"S":"0.0344",
		"SD":"2.365",
		"SD3neg":"61.7",
		"SD2neg":"64",
		"SD1neg":"66.4",
		"SD0":"68.7",
		"SD1":"71.1",
		"SD2":"73.5",
		"SD3":"75.8"
	},
	{
		"Month":"9",
		"L":"1",
		"M":"70.1435",
		"S":"0.03444",
		"SD":"2.4157",
		"SD3neg":"62.9",
		"SD2neg":"65.3",
		"SD1neg":"67.7",
		"SD0":"70.1",
		"SD1":"72.6",
		"SD2":"75",
		"SD3":"77.4"
	},
	{
		"Month":"10",
		"L":"1",
		"M":"71.4818",
		"S":"0.03452",
		"SD":"2.4676",
		"SD3neg":"64.1",
		"SD2neg":"66.5",
		"SD1neg":"69",
		"SD0":"71.5",
		"SD1":"73.9",
		"SD2":"76.4",
		"SD3":"78.9"
	},
	{
		"Month":"11",
		"L":"1",
		"M":"72.771",
		"S":"0.03464",
		"SD":"2.5208",
		"SD3neg":"65.2",
		"SD2neg":"67.7",
		"SD1neg":"70.3",
		"SD0":"72.8",
		"SD1":"75.3",
		"SD2":"77.8",
		"SD3":"80.3"
	},
	{
		"Month":"12",
		"L":"1",
		"M":"74.015",
		"S":"0.03479",
		"SD":"2.575",
		"SD3neg":"66.3",
		"SD2neg":"68.9",
		"SD1neg":"71.4",
		"SD0":"74",
		"SD1":"76.6",
		"SD2":"79.2",
		"SD3":"81.7"
	},
	{
		"Month":"13",
		"L":"1",
		"M":"75.2176",
		"S":"0.03496",
		"SD":"2.6296",
		"SD3neg":"67.3",
		"SD2neg":"70",
		"SD1neg":"72.6",
		"SD0":"75.2",
		"SD1":"77.8",
		"SD2":"80.5",
		"SD3":"83.1"
	},
	{
		"Month":"14",
		"L":"1",
		"M":"76.3817",
		"S":"0.03514",
		"SD":"2.6841",
		"SD3neg":"68.3",
		"SD2neg":"71",
		"SD1neg":"73.7",
		"SD0":"76.4",
		"SD1":"79.1",
		"SD2":"81.7",
		"SD3":"84.4"
	},
	{
		"Month":"15",
		"L":"1",
		"M":"77.5099",
		"S":"0.03534",
		"SD":"2.7392",
		"SD3neg":"69.3",
		"SD2neg":"72",
		"SD1neg":"74.8",
		"SD0":"77.5",
		"SD1":"80.2",
		"SD2":"83",
		"SD3":"85.7"
	},
	{
		"Month":"16",
		"L":"1",
		"M":"78.6055",
		"S":"0.03555",
		"SD":"2.7944",
		"SD3neg":"70.2",
		"SD2neg":"73",
		"SD1neg":"75.8",
		"SD0":"78.6",
		"SD1":"81.4",
		"SD2":"84.2",
		"SD3":"87"
	},
	{
		"Month":"17",
		"L":"1",
		"M":"79.671",
		"S":"0.03576",
		"SD":"2.849",
		"SD3neg":"71.1",
		"SD2neg":"74",
		"SD1neg":"76.8",
		"SD0":"79.7",
		"SD1":"82.5",
		"SD2":"85.4",
		"SD3":"88.2"
	},
	{
		"Month":"18",
		"L":"1",
		"M":"80.7079",
		"S":"0.03598",
		"SD":"2.9039",
		"SD3neg":"72",
		"SD2neg":"74.9",
		"SD1neg":"77.8",
		"SD0":"80.7",
		"SD1":"83.6",
		"SD2":"86.5",
		"SD3":"89.4"
	},
	{
		"Month":"19",
		"L":"1",
		"M":"81.7182",
		"S":"0.0362",
		"SD":"2.9582",
		"SD3neg":"72.8",
		"SD2neg":"75.8",
		"SD1neg":"78.8",
		"SD0":"81.7",
		"SD1":"84.7",
		"SD2":"87.6",
		"SD3":"90.6"
	},
	{
		"Month":"20",
		"L":"1",
		"M":"82.7036",
		"S":"0.03643",
		"SD":"3.0129",
		"SD3neg":"73.7",
		"SD2neg":"76.7",
		"SD1neg":"79.7",
		"SD0":"82.7",
		"SD1":"85.7",
		"SD2":"88.7",
		"SD3":"91.7"
	},
	{
		"Month":"21",
		"L":"1",
		"M":"83.6654",
		"S":"0.03666",
		"SD":"3.0672",
		"SD3neg":"74.5",
		"SD2neg":"77.5",
		"SD1neg":"80.6",
		"SD0":"83.7",
		"SD1":"86.7",
		"SD2":"89.8",
		"SD3":"92.9"
	},
	{
		"Month":"22",
		"L":"1",
		"M":"84.604",
		"S":"0.03688",
		"SD":"3.1202",
		"SD3neg":"75.2",
		"SD2neg":"78.4",
		"SD1neg":"81.5",
		"SD0":"84.6",
		"SD1":"87.7",
		"SD2":"90.8",
		"SD3":"94"
	},
	{
		"Month":"23",
		"L":"1",
		"M":"85.5202",
		"S":"0.03711",
		"SD":"3.1737",
		"SD3neg":"76",
		"SD2neg":"79.2",
		"SD1neg":"82.3",
		"SD0":"85.5",
		"SD1":"88.7",
		"SD2":"91.9",
		"SD3":"95"
	},
	{
		"Month":"24",
		"L":"1",
		"M":"86.4153",
		"S":"0.03734",
		"SD":"3.2267",
		"SD3neg":"76.7",
		"SD2neg":"80",
		"SD1neg":"83.2",
		"SD0":"86.4",
		"SD1":"89.6",
		"SD2":"92.9",
		"SD3":"96.1"
	},
	{
		"Month":"24",
		"L":"1",
		"M":"85.7153",
		"S":"0.03764",
		"SD":"3.2267",
		"SD3neg":"76",
		"SD2neg":"79.3",
		"SD1neg":"82.5",
		"SD0":"85.7",
		"SD1":"88.9",
		"SD2":"92.2",
		"SD3":"95.4"
	},
	{
		"Month":"25",
		"L":"1",
		"M":"86.5904",
		"S":"0.03786",
		"SD":"3.2783",
		"SD3neg":"76.8",
		"SD2neg":"80",
		"SD1neg":"83.3",
		"SD0":"86.6",
		"SD1":"89.9",
		"SD2":"93.1",
		"SD3":"96.4"
	},
	{
		"Month":"26",
		"L":"1",
		"M":"87.4462",
		"S":"0.03808",
		"SD":"3.33",
		"SD3neg":"77.5",
		"SD2neg":"80.8",
		"SD1neg":"84.1",
		"SD0":"87.4",
		"SD1":"90.8",
		"SD2":"94.1",
		"SD3":"97.4"
	},
	{
		"Month":"27",
		"L":"1",
		"M":"88.283",
		"S":"0.0383",
		"SD":"3.3812",
		"SD3neg":"78.1",
		"SD2neg":"81.5",
		"SD1neg":"84.9",
		"SD0":"88.3",
		"SD1":"91.7",
		"SD2":"95",
		"SD3":"98.4"
	},
	{
		"Month":"28",
		"L":"1",
		"M":"89.1004",
		"S":"0.03851",
		"SD":"3.4313",
		"SD3neg":"78.8",
		"SD2neg":"82.2",
		"SD1neg":"85.7",
		"SD0":"89.1",
		"SD1":"92.5",
		"SD2":"96",
		"SD3":"99.4"
	},
	{
		"Month":"29",
		"L":"1",
		"M":"89.8991",
		"S":"0.03872",
		"SD":"3.4809",
		"SD3neg":"79.5",
		"SD2neg":"82.9",
		"SD1neg":"86.4",
		"SD0":"89.9",
		"SD1":"93.4",
		"SD2":"96.9",
		"SD3":"100.3"
	},
	{
		"Month":"30",
		"L":"1",
		"M":"90.6797",
		"S":"0.03893",
		"SD":"3.5302",
		"SD3neg":"80.1",
		"SD2neg":"83.6",
		"SD1neg":"87.1",
		"SD0":"90.7",
		"SD1":"94.2",
		"SD2":"97.7",
		"SD3":"101.3"
	},
	{
		"Month":"31",
		"L":"1",
		"M":"91.443",
		"S":"0.03913",
		"SD":"3.5782",
		"SD3neg":"80.7",
		"SD2neg":"84.3",
		"SD1neg":"87.9",
		"SD0":"91.4",
		"SD1":"95",
		"SD2":"98.6",
		"SD3":"102.2"
	},
	{
		"Month":"32",
		"L":"1",
		"M":"92.1906",
		"S":"0.03933",
		"SD":"3.6259",
		"SD3neg":"81.3",
		"SD2neg":"84.9",
		"SD1neg":"88.6",
		"SD0":"92.2",
		"SD1":"95.8",
		"SD2":"99.4",
		"SD3":"103.1"
	},
	{
		"Month":"33",
		"L":"1",
		"M":"92.9239",
		"S":"0.03952",
		"SD":"3.6724",
		"SD3neg":"81.9",
		"SD2neg":"85.6",
		"SD1neg":"89.3",
		"SD0":"92.9",
		"SD1":"96.6",
		"SD2":"100.3",
		"SD3":"103.9"
	},
	{
		"Month":"34",
		"L":"1",
		"M":"93.6444",
		"S":"0.03971",
		"SD":"3.7186",
		"SD3neg":"82.5",
		"SD2neg":"86.2",
		"SD1neg":"89.9",
		"SD0":"93.6",
		"SD1":"97.4",
		"SD2":"101.1",
		"SD3":"104.8"
	},
	{
		"Month":"35",
		"L":"1",
		"M":"94.3533",
		"S":"0.03989",
		"SD":"3.7638",
		"SD3neg":"83.1",
		"SD2neg":"86.8",
		"SD1neg":"90.6",
		"SD0":"94.4",
		"SD1":"98.1",
		"SD2":"101.9",
		"SD3":"105.6"
	},
	{
		"Month":"36",
		"L":"1",
		"M":"95.0515",
		"S":"0.04006",
		"SD":"3.8078",
		"SD3neg":"83.6",
		"SD2neg":"87.4",
		"SD1neg":"91.2",
		"SD0":"95.1",
		"SD1":"98.9",
		"SD2":"102.7",
		"SD3":"106.5"
	},
	{
		"Month":"37",
		"L":"1",
		"M":"95.7399",
		"S":"0.04024",
		"SD":"3.8526",
		"SD3neg":"84.2",
		"SD2neg":"88",
		"SD1neg":"91.9",
		"SD0":"95.7",
		"SD1":"99.6",
		"SD2":"103.4",
		"SD3":"107.3"
	},
	{
		"Month":"38",
		"L":"1",
		"M":"96.4187",
		"S":"0.04041",
		"SD":"3.8963",
		"SD3neg":"84.7",
		"SD2neg":"88.6",
		"SD1neg":"92.5",
		"SD0":"96.4",
		"SD1":"100.3",
		"SD2":"104.2",
		"SD3":"108.1"
	},
	{
		"Month":"39",
		"L":"1",
		"M":"97.0885",
		"S":"0.04057",
		"SD":"3.9389",
		"SD3neg":"85.3",
		"SD2neg":"89.2",
		"SD1neg":"93.1",
		"SD0":"97.1",
		"SD1":"101",
		"SD2":"105",
		"SD3":"108.9"
	},
	{
		"Month":"40",
		"L":"1",
		"M":"97.7493",
		"S":"0.04073",
		"SD":"3.9813",
		"SD3neg":"85.8",
		"SD2neg":"89.8",
		"SD1neg":"93.8",
		"SD0":"97.7",
		"SD1":"101.7",
		"SD2":"105.7",
		"SD3":"109.7"
	},
	{
		"Month":"41",
		"L":"1",
		"M":"98.4015",
		"S":"0.04089",
		"SD":"4.0236",
		"SD3neg":"86.3",
		"SD2neg":"90.4",
		"SD1neg":"94.4",
		"SD0":"98.4",
		"SD1":"102.4",
		"SD2":"106.4",
		"SD3":"110.5"
	},
	{
		"Month":"42",
		"L":"1",
		"M":"99.0448",
		"S":"0.04105",
		"SD":"4.0658",
		"SD3neg":"86.8",
		"SD2neg":"90.9",
		"SD1neg":"95",
		"SD0":"99",
		"SD1":"103.1",
		"SD2":"107.2",
		"SD3":"111.2"
	},
	{
		"Month":"43",
		"L":"1",
		"M":"99.6795",
		"S":"0.0412",
		"SD":"4.1068",
		"SD3neg":"87.4",
		"SD2neg":"91.5",
		"SD1neg":"95.6",
		"SD0":"99.7",
		"SD1":"103.8",
		"SD2":"107.9",
		"SD3":"112"
	},
	{
		"Month":"44",
		"L":"1",
		"M":"100.3058",
		"S":"0.04135",
		"SD":"4.1476",
		"SD3neg":"87.9",
		"SD2neg":"92",
		"SD1neg":"96.2",
		"SD0":"100.3",
		"SD1":"104.5",
		"SD2":"108.6",
		"SD3":"112.7"
	},
	{
		"Month":"45",
		"L":"1",
		"M":"100.9238",
		"S":"0.0415",
		"SD":"4.1883",
		"SD3neg":"88.4",
		"SD2neg":"92.5",
		"SD1neg":"96.7",
		"SD0":"100.9",
		"SD1":"105.1",
		"SD2":"109.3",
		"SD3":"113.5"
	},
	{
		"Month":"46",
		"L":"1",
		"M":"101.5337",
		"S":"0.04164",
		"SD":"4.2279",
		"SD3neg":"88.9",
		"SD2neg":"93.1",
		"SD1neg":"97.3",
		"SD0":"101.5",
		"SD1":"105.8",
		"SD2":"110",
		"SD3":"114.2"
	},
	{
		"Month":"47",
		"L":"1",
		"M":"102.136",
		"S":"0.04179",
		"SD":"4.2683",
		"SD3neg":"89.3",
		"SD2neg":"93.6",
		"SD1neg":"97.9",
		"SD0":"102.1",
		"SD1":"106.4",
		"SD2":"110.7",
		"SD3":"114.9"
	},
	{
		"Month":"48",
		"L":"1",
		"M":"102.7312",
		"S":"0.04193",
		"SD":"4.3075",
		"SD3neg":"89.8",
		"SD2neg":"94.1",
		"SD1neg":"98.4",
		"SD0":"102.7",
		"SD1":"107",
		"SD2":"111.3",
		"SD3":"115.7"
	},
	{
		"Month":"49",
		"L":"1",
		"M":"103.3197",
		"S":"0.04206",
		"SD":"4.3456",
		"SD3neg":"90.3",
		"SD2neg":"94.6",
		"SD1neg":"99",
		"SD0":"103.3",
		"SD1":"107.7",
		"SD2":"112",
		"SD3":"116.4"
	},
	{
		"Month":"50",
		"L":"1",
		"M":"103.9021",
		"S":"0.0422",
		"SD":"4.3847",
		"SD3neg":"90.7",
		"SD2neg":"95.1",
		"SD1neg":"99.5",
		"SD0":"103.9",
		"SD1":"108.3",
		"SD2":"112.7",
		"SD3":"117.1"
	},
	{
		"Month":"51",
		"L":"1",
		"M":"104.4786",
		"S":"0.04233",
		"SD":"4.4226",
		"SD3neg":"91.2",
		"SD2neg":"95.6",
		"SD1neg":"100.1",
		"SD0":"104.5",
		"SD1":"108.9",
		"SD2":"113.3",
		"SD3":"117.7"
	},
	{
		"Month":"52",
		"L":"1",
		"M":"105.0494",
		"S":"0.04246",
		"SD":"4.4604",
		"SD3neg":"91.7",
		"SD2neg":"96.1",
		"SD1neg":"100.6",
		"SD0":"105",
		"SD1":"109.5",
		"SD2":"114",
		"SD3":"118.4"
	},
	{
		"Month":"53",
		"L":"1",
		"M":"105.6148",
		"S":"0.04259",
		"SD":"4.4981",
		"SD3neg":"92.1",
		"SD2neg":"96.6",
		"SD1neg":"101.1",
		"SD0":"105.6",
		"SD1":"110.1",
		"SD2":"114.6",
		"SD3":"119.1"
	},
	{
		"Month":"54",
		"L":"1",
		"M":"106.1748",
		"S":"0.04272",
		"SD":"4.5358",
		"SD3neg":"92.6",
		"SD2neg":"97.1",
		"SD1neg":"101.6",
		"SD0":"106.2",
		"SD1":"110.7",
		"SD2":"115.2",
		"SD3":"119.8"
	},
	{
		"Month":"55",
		"L":"1",
		"M":"106.7295",
		"S":"0.04285",
		"SD":"4.5734",
		"SD3neg":"93",
		"SD2neg":"97.6",
		"SD1neg":"102.2",
		"SD0":"106.7",
		"SD1":"111.3",
		"SD2":"115.9",
		"SD3":"120.4"
	},
	{
		"Month":"56",
		"L":"1",
		"M":"107.2788",
		"S":"0.04298",
		"SD":"4.6108",
		"SD3neg":"93.4",
		"SD2neg":"98.1",
		"SD1neg":"102.7",
		"SD0":"107.3",
		"SD1":"111.9",
		"SD2":"116.5",
		"SD3":"121.1"
	},
	{
		"Month":"57",
		"L":"1",
		"M":"107.8227",
		"S":"0.0431",
		"SD":"4.6472",
		"SD3neg":"93.9",
		"SD2neg":"98.5",
		"SD1neg":"103.2",
		"SD0":"107.8",
		"SD1":"112.5",
		"SD2":"117.1",
		"SD3":"121.8"
	},
	{
		"Month":"58",
		"L":"1",
		"M":"108.3613",
		"S":"0.04322",
		"SD":"4.6834",
		"SD3neg":"94.3",
		"SD2neg":"99",
		"SD1neg":"103.7",
		"SD0":"108.4",
		"SD1":"113",
		"SD2":"117.7",
		"SD3":"122.4"
	},
	{
		"Month":"59",
		"L":"1",
		"M":"108.8948",
		"S":"0.04334",
		"SD":"4.7195",
		"SD3neg":"94.7",
		"SD2neg":"99.5",
		"SD1neg":"104.2",
		"SD0":"108.9",
		"SD1":"113.6",
		"SD2":"118.3",
		"SD3":"123.1"
	},
	{
		"Month":"60",
		"L":"1",
		"M":"109.4233",
		"S":"0.04347",
		"SD":"4.7566",
		"SD3neg":"95.2",
		"SD2neg":"99.9",
		"SD1neg":"104.7",
		"SD0":"109.4",
		"SD1":"114.2",
		"SD2":"118.9",
		"SD3":"123.7"
	}
];


	lhfa_boys_0_to_5 = {
		"meta" : lhfa_boys_0_to_5_meta,
		"data" : lhfa_boys_0_to_5_zscores
	};

	lhfa_girls_0_to_5 = {
		"meta" : lhfa_girls_0_to_5_meta,
		"data" : lhfa_girls_0_to_5_zscores
	};



};

////////////////////////////////
// Chart
////////////////////////////////

var defaultStuntingConf = {
	height: 325,
	titles: true,
  padding: 40,
	extraRightPadding: 60,
	lhfa_all_0_to_5_meta: {
    "lines": [{
      "tag":"SD0",
      "name":"50th"
    }, {
      "tag":"SD1neg",
      "name":"15th"
    }, {
      "tag":"SD2neg",
      "name":"2nd"
    }, {
      "tag":"SD2",
      "name":"98th"
    }, {
      "tag":"SD1",
      "name":"85th"
    }, {
      "tag":"SD3",
      "name":"99.9th"
    }, {
      "tag":"SD3neg",
      "name":"0.1th"
    }]},
	
};

function display_stunting_chart(growthData, el, chartType, config) {
  // TODO replace with vanillajs and get rid of underscore
	var conf = _.defaults(config, defaultConf);
	prepStuntingData(conf);

  // Create the background lines
  //
  // json includes "meta" (to tag+name the lines, specify measurement type)
  //  and "data" (containing age in months vs measurement)
  function createLines(json) {
    var meta = json.meta;
    var data = json.data;

    var newLines = [];

    for (var i=0; i < meta.lines.length; i++) {
      // Get the tag
      var lineTag = meta.lines[i].tag;

      newLines.push([]);
      // Generate the list of data (month, measurement)
      for (var j=0; j < data.length; j++) {
        // Assumes data has a "Month" tag in each element
        newLines[i].push([data[j]["Month"], data[j][lineTag]]);
      }
    }
    return newLines;
  }

  // Get data to build chart's 'background lines' depending on chartType
  var data;
  var metaData;
  var chartTypes = {
    'lhfa_boys_0_to_5' : lhfa_boys_0_to_5,
    'lhfa_girls_0_to_5': lhfa_girls_0_to_5,
    
  };

  // NOTE this is in the global scope so that the 
  // changeGraphType code can be in outside of this file
  chartTypeKeys = [];
  for (k in chartTypes) {
    if (chartTypes.hasOwnProperty(k)) {
      chartTypeKeys.push(k);
    }
  }

  if (chartTypes.hasOwnProperty(chartType)) {
    data = createLines(chartTypes[chartType]);
    metaData = chartTypes[chartType].meta;
  } else {
    console.log('Error choosing chart type. Your input was "' + chartType + '". Valid options are:', chartTypeKeys);
    return;
  }

  // Save the last tuple so that I can label it
  lastTuples = [];

  // Boundaries for graph, based on growth chart bounds
  var yMax = 0; // height, in cm
  var xMax = 0; // age, in months
  for (var i = 0; i < data.length; i++) {
    var lineData = data[i];
    var lastTuple = lineData[lineData.length-1];
    lastTuples.push(lastTuple);
    xMax = Math.max(lastTuple[0], xMax);
    yMax = Math.max(lastTuple[1], yMax);
  }

  // Graph formatting, in pixels
	var golden = ((1 + Math.sqrt(5)) / 2); // golden ratio FTW
  // NOTE these are in the global scope so that the 
  // changeGraphType code can be in outside of this file
  width = conf.height * golden;

  // Graph scale; domain and range
  var xScale = d3.scale.linear()
    .domain([0, xMax])
    .range([conf.padding, width - conf.padding]);

  var yScale = d3.scale.linear()
    .domain([0, yMax])
    .range([conf.height - conf.padding, conf.padding]);

  // Line generating function
  var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d, i) { return xScale(d[0]); })
    .y(function(d) { return yScale(d[1]); });

  // Area under the curve, for highlighting regions
  var area = d3.svg.area()
    .interpolate("basis")
    .x(line.x())
    .y1(line.y())
    .y0(yScale(0));

  // clear exiting growth chart svg .. allows to reset graph with new background
  d3.select(el).select(".growth_chart_main_svg").remove();

  // FIXME this is in the global scope so that the 
  // changeGraphType code can be outside of this file.
  svg = d3.select(el).append("svg")
    .attr("width", width + conf.extraRightPadding)
    .attr("height", conf.height)
    .attr("class", "growth_chart_main_svg");

  // add a monocolor background
  var backgroundRect = svg.append("g");
  backgroundRect.append("rect")
    .attr("width", width + conf.extraRightPadding)
    .attr("height", conf.height)
    .attr("class", "backgroundRect");

	var green = "#6AE272";
	var yellow = "#FFDB66";
	var red = "#FF8F8F";
	var color = d3.scale.ordinal();
  // TODO replace with vanillajs and get rid of underscore
  if (_.find(['lhfa_boys_0_to_5', 'lhfa_girls_0_to_5'], function(k) { return k === chartType; })){
	  color.domain([0, 1, 2, 3, 4, 5, 6])
			.range([red, yellow, green, green, yellow, red, red]);
	}

  // Baseline growth curves
  var curves = svg.append("g")
		.attr("class", "curves")
		.selectAll(".curve")
			// sort the data so we start with 3 SD curve -- draw order is important!
      // TODO replace with vanillajs and get rid of underscore
			.data(_.sortBy(data, function(l) { return l[10][1]; }).reverse())
			.enter();

	var curve = curves.append("g")
		.attr("class", function(d, i) { return "curve curve-" + i; });

	curve.append("path")
			.attr("class", "area")
			.attr("fill", function(d, i) { return color(i); })
			.attr("d", area);

	curve.append("path")
			.attr("class", "line")
			.attr("d", line);

	// add group before other stuff so we can clear it after hover
  var linesToAxis = svg.append("g");

  // Patient's data
  // TODO replace with vanillajs and get rid of underscore
	var patientData = _.map(growthData, function(p) {return [p.age, p.height];});
	// see if we have data on one patient or many patients
	// so we can draw a scatterplot for many and a line chart for one
  // TODO replace with vanillajs and get rid of underscore
	var onlyOnePatient = (_.unique(_.pluck(growthData, 'id')).length === 1);

  // Add line for the patient's growth if all data is for same patient
	if (onlyOnePatient) {
		var linesP = svg.selectAll("pG")
			.data([patientData])
			.attr("class", "pG")
			.enter();
		linesP.append("path")
			.attr("class", "pLine")
			.attr("d", line.interpolate("")); // interpolate("") removes the smoothing
	}

  // Dots at each data point
  var dots = svg.append("g")
		.attr("class", "dots")
		.selectAll(".dot")
			.data(growthData)
		.enter()
			.append("svg:a")
			  .attr("xlink:href", function(d) { return "/tables/childgrowth?pid=" + d.id; })
			.append("circle")
			.attr("class", "dot")
		.call(dotStuntingHandler(function(d, i) {
			return getStuntingTooltipText(d);
		}))
		.attr("cx", function(d, i) {
			return xScale(d.age);
		})
			.attr("cy", function(d, i) {
			return yScale(d.height);
		})
			.attr("r", 3);

  // Add axes

  // x-axis
  var xAxis = d3.svg.axis();
  xAxis.scale(xScale)
		.orient("bottom")
    .tickSubdivide(3)
		.tickSize(6, 3, 0)
		.tickValues(d3.range(12, 72, 12));

  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + 0 + "," + (conf.height - conf.padding) + ")")
    .call(xAxis);

  // y-axis
  var yAxis = d3.svg.axis();
  yAxis.scale(yScale);
  yAxis.orient("left")
    .ticks(8);

  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + conf.padding + ",0)")
    .call(yAxis);

  // Axes text
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ (conf.padding/3) +","+(conf.height-conf.padding)/2+")rotate(-90)")
    .text("Height (cm)");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ (width/2) +","+(conf.height-(conf.padding/3))+")")
    .text("Age (months)");

  // Line labels (Normal, Malnourished, and Severely Malnourished)
  for (var i=0; i<metaData.lines.length; i++) {
    xOffset = xScale(lastTuples[i][0]);
    xOffset += 2; // a little space better graph and text
    yOffset = yScale(lastTuples[i][1]);
    yOffset += 4; // center text on line

    svg.append("text")
      .attr("class","line-label")
      .attr("transform", "translate("+ xOffset +","+ yOffset +")")
      .text(metaData.lines[i].name);
  }

  var tooltipOffset = conf.padding - 10;
  var tooltipGroup = svg.append("g").attr("class", "tooltip");

  var tooltipText = tooltipGroup.append("text")
    .attr("x", tooltipOffset)
    .attr("y", tooltipOffset)
    .attr("class","tooltipText")
    .style("font-size","14px")
    .text("");

	if (conf.titles) {
		svg.append("text")
					.attr("x", (width / 2))
					.attr("y", 0 + (conf.padding / 2))
					.attr("text-anchor", "middle")
					.style("font-size", "16px")
					.text(metaData.title);
	};

  function dotStuntingHandler(accessor) {
    return function(selection) {
      selection.on("mouseover", function(d, i) {
        // Select current dot, unselect others
        d3.selectAll("circle.dotSelected").attr("class", "dot");
        d3.select(this).attr("class", "dotSelected");

        // Update text using the accessor function
        var ttAccessor = accessor(d, i) || '';
        tooltipText.text(ttAccessor);

        // Update text background
        var dottedSegmentLength = 3;  // used below, too, for linesToAxis

        // create a rectangle that stretches to the axes, so it's easy to see if the axis is right..
        // Remove old
				// TODO use .classed('hidden') rather than removing rect from DOM
				// TODO draw lines instead of a rect
        linesToAxis.selectAll(".rect-to-axis")
          .data([])
        .exit().remove();

        // Add new
        var linesToAxisWidth = xScale(d.age) - conf.padding;
        var linesToAxisHeight = conf.height - yScale(d.height) - conf.padding;
        var halfRectLength = linesToAxisWidth + linesToAxisHeight;
        halfRect = halfRectLength.toString();

        // Draw top and right sides of rectangle as dotted. Hide bottom and left sides
        var dottedSegments = Math.floor(halfRectLength / dottedSegmentLength);
        var nonDottedLength = halfRectLength*2; // + (dottedSegments % dottedSegmentLength);

        var dashArrayStroke = [];

        for (var i=0; i < dottedSegments; i++) {
          dashArrayStroke.push(dottedSegmentLength);
        }
        // if even number, add extra filler segment to make sure 2nd half of rectangle is hidden
        if ( (dottedSegments % 2) === 0) {
          extraSegmentLength = halfRectLength - (dottedSegments*dottedSegmentLength);
          dashArrayStroke.push(extraSegmentLength);
          dashArrayStroke.push(nonDottedLength);
        } else {
          dashArrayStroke.push(nonDottedLength);
        }

        linesToAxis.selectAll(".rect-to-axis")
          .data([d.age, d.height])
         .enter().append("rect")
          .attr("class", "rect-to-axis")
          .style("stroke-dasharray",
            dashArrayStroke.toString()
          )
          .attr("x", conf.padding)
          .attr("y", yScale(d.height))
          .attr("width", linesToAxisWidth)
          .attr("height", linesToAxisHeight);

      });
    };
  }

  function getStuntingTooltipText(d) {
    var age_in_months = parseFloat(d.age);
    var height_in_cm = parseFloat(d.height).toFixed(1);
    var textAge = 'Age: ' + getStuntingAgeText(age_in_months);
    var textheight = 'Height: ' + height_in_cm + 'cm';
		var text = textAge + '; ' + textheight;

		// if `id` is present, add `id` to tooltip text
		if (d.hasOwnProperty('id')){
			text = 'Child ' + d.id + ': ' + text;
		}

    return text;
  }

  // @param months - age in months (float)
  // @return - age (<years>y, <months>m) (string)

  function getStuntingAgeText(months){
    var y = Math.floor(months / 12);
    var m = months - (y * 12);
    m = m.toFixed(1);

    if (y > 0) {
      return y + 'y, ' + m + 'm';
    } else {
      return m + 'm';
    }
  }

  // callable methods
  return this;
}
