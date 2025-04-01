const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
var adres = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?endeks=01#page-1";

async function scrapeData() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(adres);

    const content = await page.content();
    const $ = cheerio.load(content);

    //const hisses = [];

    var kod = $(`#temelTBody_Ozet > tr:nth-child(2) > td.sorting_1 > a`).text().trim();
    console.log(kod);
    /*
    for (let i = 1; i <= 100; i++) {
        const hisse = {
            kod: $(`tr:nth-child(${i}) .hisseKoduSelector`).text().trim(),
            f_k: parseFloat($(`tr:nth-child(${i}) .fkSelector`).text().trim()),
            // Diğer oranlar için benzer kodları buraya ekleyin
        };
        hisses.push(hisse);
    }
    

    

    // Veriyi işleyip veya kaydedip dilediğiniz diğer işlemleri burada yapabilirsiniz
    hisses.forEach(hisse => {
        // Örneğin, console'a yazdırabilirsiniz
        console.log(hisse);
    });
    */
    await browser.close();

};

scrapeData();