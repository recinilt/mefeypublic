const axios = require('axios');
const cheerio = require('cheerio');

async function getWebsiteTitle() {
    /*
    const response = await axios.get(url);
    const html = response.data;
    const $ = cheerio.load(html);
    
    const title = $('head > title').text();

    return title;
    */
    /////////////////////////
    //document.querySelector("body > main > div.master.flex.w-full.justify-center.items-start > div.w-full.min-w-full > section:nth-child(2) > div.overflow-x-auto.mb-5.border.dark\\:border-gray-800 > table > tbody > tr:nth-child(1) > td.px-4.py-4.bg-white.border-dashed.border-b.dark\\:bg-gray-900.dark\\:border-gray-800.sticky.left-0 > div > a > span.text-sm")
    var urlbist100 = "https://www.haberturk.com/ekonomi/borsa/bist-100";
    const response = await axios.get(urlbist100);
    const html = response.data;
    var $ = cheerio.load(html);


    var adres = "";
    var hisse = "";
    var bist100 = [];
    for (let index = 1; index < 101; index++) {
        adres = 'body > main > div.master.flex.w-full.justify-center.items-start > div.w-full.min-w-full > section:nth-child(2) > div.overflow-x-auto.mb-5.border.dark\\:border-gray-800 > table > tbody > tr:nth-child(' + index + ') > td.px-4.py-4.bg-white.border-dashed.border-b.dark\\:bg-gray-900.dark\\:border-gray-800.sticky.left-0 > div > a > span.text-sm';
        hisse = $(adres).text();
        bist100.push(hisse);
        
        
    };

    /*
    var urlhisse = "";
    var responsehisse = "";
    var htmlhisse = "";
    

    var pddd = [];
    var dd = [];
    var pddddd = [];
    for (let index = 0; index < 100; index++) {
        urlhisse = "https://www.borsagundem.com.tr/piyasa-ekrani/hisse-detay/" + bist100[index];
        responsehisse = await axios.get(urlhisse);
        htmlhisse = responsehisse.data;
        $ = cheerio.load(htmlhisse);
        
        pddd.push($('#wrap > div.hisdtl > div.dtb1 > ul > li.s6 > span').text());
        dd.push($('#wrap > div.hisdtl > div.dtb1 > ul > li.s3 > span').text());
        pddddd.push(pddd/dd);
        
    };

    console.log(pddddd);
    */
    return bist100;

};

getWebsiteTitle().then(bist100listesi => {
    console.log(bist100listesi);
    console.log(bist100listesi.length);
});