/* ═══════════════════════════════════════════════════════════════
   PRINT PRO SG — Product Configurator  v27
   product.js
═══════════════════════════════════════════════════════════════ */

/* ─── Delivery date helpers ─── */
function addBusinessDays(date, n) {
  const d = new Date(date);
  let added = 0;
  while (added < n) {
    d.setDate(d.getDate() + 1);
    if (d.getDay() !== 0 && d.getDay() !== 6) added++;
  }
  return d;
}
function fmtDate(d) {
  const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return `${days[d.getDay()]}, ${d.getDate()} ${months[d.getMonth()]}`;
}
const TODAY = new Date();
const DELIVERY_COLS = [
  { label: fmtDate(addBusinessDays(TODAY, 1)), badge: 'fastest', days: 1 },
  { label: fmtDate(addBusinessDays(TODAY, 3)), badge: '',         days: 3 },
  { label: fmtDate(addBusinessDays(TODAY, 5)), badge: 'cheapest', days: 5 },
];

/* ─── GST state ─── */
let gstOn = false;
function toggleGST() {
  gstOn = document.getElementById('gst-toggle').checked;
  renderPricingTable();
}

/* ═══════════════════════════════════════════════════════════════
   PRODUCT DATABASE
═══════════════════════════════════════════════════════════════ */
const PRODUCTS = {

  'name-cards': {
    name: 'Name Cards',
    category: 'Name Cards',
    img: 'img/services/name_card.jpg',
    basePrice: 30, origPrice: 52, discount: 42,
    description: `<p>Name cards are one of the most powerful networking tools for any business professional. Our premium name cards are printed on high-quality paper stocks with a variety of finishes to make your first impression count.</p><p>At Print Pro SG, we offer fast turnaround with same-day delivery available for urgent orders.</p>`,
    specs: [['Standard Size','90 x 54 mm'],['Paper Options','310gsm, 350gsm, 400gsm Art Card'],['Finishes','Matte, Gloss, Spot UV, Soft Touch'],['Sides','Single Side, Double Side'],['Min. Order','50 pcs'],['Turnaround','1-5 business days']],
    faq: [
      {q:'What file format should I upload?',a:'Please upload PDF files in CMYK colour mode with 3mm bleed on all sides.'},
      {q:'Can I order different designs in one batch?',a:'Yes, please contact us for bulk multi-design orders.'},
      {q:'Is same-day delivery available?',a:'Yes, same-day delivery is available for orders placed before 11am on weekdays.'},
    ],
    options: [
      {id:'size',   label:'FORMAT',              choices:['9 x 5.4 cm (Standard)','5.5 x 9 cm (Vertical)','8.5 x 5.5 cm (Mini)','5.4 x 9 cm (Slim)']},
      {id:'sides',  label:'SIDE OF PRINT',       choices:['Full Colour Front & Back','Full Colour Front Only','Black & White Front & Back','Black & White Front Only']},
      {id:'paper',  label:'PAPER STOCK',         choices:['310gsm Art Card','350gsm Premium Card','400gsm Thick Card','450gsm Ultra Thick']},
      {id:'finish', label:'LAMINATION / FINISH', choices:['None','Gloss Lamination','Matte Lamination','Soft Touch Matte','Spot UV (Front)']},
      {id:'corners',label:'ROUNDED CORNERS',     choices:['No Rounded Corners','Rounded Corners (+$2)']},
      {id:'holder', label:'CARD HOLDER',         choices:['None','Acrylic Card Holder (+$8)','Metal Card Holder (+$15)']},
    ],
    quantities: [50,100,200,300,500,1000,2000,3000,5000],
    pricingMatrix: {50:[30,22,18],100:[41,30,24],200:[55,41,33],300:[68,51,41],500:[95,72,58],1000:[145,110,88],2000:[220,166,133],3000:[295,222,178],5000:[440,330,264]},
    origMatrix:    {50:[52,38,31],100:[71,52,41],200:[95,71,57],300:[117,88,71],500:[164,124,100],1000:[250,190,152],2000:[379,286,229],3000:[508,382,307],5000:[758,569,455]},
    related: ['stickers','flyers','postcards','brochures'],
  },

  'stickers': {
    name: 'Stickers & Labels',
    category: 'Stickers',
    img: 'img/services/sticker_label.jpg',
    basePrice: 18, origPrice: 35, discount: 49,
    description: `<p>Custom stickers and labels are perfect for branding, packaging, promotions, and events. Our stickers are printed on premium vinyl or paper stock with a strong adhesive backing.</p>`,
    specs: [['Material','Vinyl, Matte Paper, Gloss Paper, Transparent'],['Shapes','Rectangle, Circle, Square, Custom Die-Cut'],['Sizes','A4 Sheet, A5 Sheet, Custom Sizes'],['Finish','Gloss, Matte, Transparent'],['Min. Order','50 pcs'],['Turnaround','1-5 business days']],
    faq: [
      {q:'Are your stickers waterproof?',a:'Our vinyl stickers are waterproof and UV-resistant, ideal for outdoor use.'},
      {q:'Can I get custom shapes?',a:'Yes, we offer die-cut stickers in any custom shape.'},
    ],
    options: [
      {id:'size',    label:'SIZE',     choices:['A4 Sheet (210x297mm)','A5 Sheet (148x210mm)','10x10 cm Square','7.5x5 cm Rectangle','Custom Size']},
      {id:'material',label:'MATERIAL', choices:['Gloss Paper','Matte Paper','White Vinyl','Transparent Vinyl','Holographic']},
      {id:'shape',   label:'SHAPE',    choices:['Rectangle','Circle','Square','Oval','Custom Die-Cut (+$5)']},
      {id:'finish',  label:'FINISH',   choices:['Gloss','Matte','Soft Touch']},
    ],
    quantities: [50,100,200,500,1000,2000,5000],
    pricingMatrix: {50:[18,14,11],100:[28,21,17],200:[42,32,26],500:[72,54,43],1000:[110,83,66],2000:[175,131,105],5000:[360,270,216]},
    origMatrix:    {50:[35,27,21],100:[55,41,33],200:[82,62,50],500:[140,105,84],1000:[214,161,129],2000:[340,255,204],5000:[699,524,419]},
    related: ['name-cards','flyers','postcards','gift-vouchers'],
  },

  'flyers': {
    name: 'Flyers & Leaflets',
    category: 'Flyers & Leaflets',
    img: 'img/services/flyer.jpg',
    basePrice: 25, origPrice: 65, discount: 62,
    description: `<p>Flyers and leaflets are the most cost-effective way to promote your business, event, or product. Our flyers are printed on high-quality art paper with vibrant full-colour printing.</p>`,
    specs: [['Sizes','A4, A5, A6, DL'],['Paper','115gsm, 128gsm, 150gsm, 170gsm Art Paper'],['Sides','Single Side, Double Side'],['Finish','Gloss, Matte'],['Min. Order','100 pcs'],['Turnaround','1-5 business days']],
    faq: [
      {q:'What sizes are available?',a:'We offer A4, A5, A6, and DL sizes as standard. Custom sizes are available on request.'},
      {q:'Can I get double-sided printing?',a:'Yes, double-sided printing is available at a small additional cost.'},
    ],
    options: [
      {id:'size',  label:'SIZE',         choices:['A4 (210x297mm)','A5 (148x210mm)','A6 (105x148mm)','DL (99x210mm)','1/3 A4 (99x210mm)']},
      {id:'sides', label:'SIDE OF PRINT',choices:['Single Side','Double Side (+$3)']},
      {id:'paper', label:'PAPER STOCK',  choices:['115gsm Art Paper','128gsm Art Paper','150gsm Art Paper','170gsm Art Paper']},
      {id:'finish',label:'FINISH',       choices:['Gloss','Matte']},
    ],
    quantities: [100,250,500,1000,2000,5000,10000],
    pricingMatrix: {100:[25,19,15],250:[38,29,23],500:[55,41,33],1000:[80,60,48],2000:[130,98,78],5000:[270,203,162],10000:[460,345,276]},
    origMatrix:    {100:[65,49,39],250:[100,75,60],500:[144,108,86],1000:[210,158,126],2000:[342,257,205],5000:[711,534,427],10000:[1211,909,727]},
    related: ['name-cards','booklets','brochures','postcards'],
  },

  'booklets': {
    name: 'Booklets',
    category: 'Booklets',
    img: 'img/services/booklet.jpg',
    basePrice: 80, origPrice: null, discount: 0,
    description: `<p>Booklets are ideal for product catalogues, company profiles, event programmes, and training manuals. Our booklets are saddle-stitched or perfect-bound for a professional finish.</p>`,
    specs: [['Sizes','A4, A5, Square'],['Pages','8, 12, 16, 20, 24, 32, 40, 48, 64 pages'],['Cover Paper','250gsm, 300gsm Art Card'],['Inner Paper','115gsm, 128gsm, 150gsm Art Paper'],['Binding','Saddle Stitch, Perfect Bind'],['Min. Order','5 pcs']],
    faq: [
      {q:'What is the minimum page count?',a:'Minimum is 8 pages (including cover) for saddle-stitch binding.'},
      {q:'Can I mix paper stocks?',a:'Yes, you can have a different paper stock for the cover and inner pages.'},
    ],
    options: [
      {id:'size',   label:'SIZE',            choices:['A4 (210x297mm)','A5 (148x210mm)','Square (148x148mm)']},
      {id:'pages',  label:'NUMBER OF PAGES', choices:['8 pages','12 pages','16 pages','20 pages','24 pages','32 pages','40 pages','48 pages','64 pages']},
      {id:'cover',  label:'COVER PAPER',     choices:['250gsm Gloss Art Card','300gsm Gloss Art Card','250gsm Matte Art Card']},
      {id:'inner',  label:'INNER PAPER',     choices:['115gsm Gloss Art Paper','128gsm Gloss Art Paper','150gsm Matte Art Paper']},
      {id:'binding',label:'BINDING',         choices:['Saddle Stitch','Perfect Bind (+$15)']},
    ],
    quantities: [5,10,25,50,100,250,500],
    pricingMatrix: {5:[80,65,55],10:[120,95,80],25:[220,175,145],50:[380,295,245],100:[620,480,400],250:[1350,1050,880],500:[2400,1850,1550]},
    origMatrix:    {5:[null,null,null],10:[null,null,null],25:[null,null,null],50:[null,null,null],100:[null,null,null],250:[null,null,null],500:[null,null,null]},
    related: ['flyers','brochures','name-cards','stickers'],
  },

  'roll-up-banners': {
    name: 'Roll-up Banners',
    category: 'Displays & Banners',
    img: 'img/services/rollup_banner.jpg',
    basePrice: 65, origPrice: 70, discount: 8,
    description: `<p>Roll-up banners are the go-to display solution for exhibitions, trade shows, retail stores, and corporate events. Lightweight, portable, and easy to set up in seconds.</p>`,
    specs: [['Standard Size','85cm x 200cm'],['Wide Size','100cm x 200cm, 120cm x 200cm'],['Material','PVC Banner, Polyester Fabric'],['Stand','Aluminium Roll-up Stand included'],['Bag','Carry bag included'],['Min. Order','1 pcs']],
    faq: [
      {q:'Does the stand come included?',a:'Yes, all roll-up banners include an aluminium stand and carry bag.'},
      {q:'Can I replace just the banner graphic?',a:'Yes, replacement graphics are available.'},
    ],
    options: [
      {id:'size',    label:'SIZE',       choices:['85cm x 200cm (Standard)','100cm x 200cm (Wide)','120cm x 200cm (Extra Wide)','60cm x 160cm (Compact)']},
      {id:'material',label:'MATERIAL',   choices:['PVC Banner (Standard)','Polyester Fabric (Premium)','Blockout PVC (No See-Through)']},
      {id:'stand',   label:'STAND TYPE', choices:['Standard Aluminium Stand','Premium Retractable Stand (+$15)','Double-Sided Stand (+$30)']},
    ],
    quantities: [1,2,3,5,10,20,50],
    pricingMatrix: {1:[65,55,48],2:[120,100,88],3:[170,142,124],5:[270,225,196],10:[490,408,356],20:[880,733,640],50:[1950,1625,1420]},
    origMatrix:    {1:[70,60,52],2:[130,108,95],3:[185,154,135],5:[294,245,214],10:[533,444,388],20:[957,798,697],50:[2120,1767,1544]},
    related: ['fabric-displays','vinyl-banners','popup-display','foam-board'],
  },

  'fabric-displays': {
    name: 'Fabric Displays',
    category: 'Displays & Banners',
    img: 'img/services/banner.jpg',
    basePrice: 239.80, origPrice: 252.50, discount: 5,
    description: `<p>Fabric displays offer a premium, wrinkle-resistant alternative to traditional banner printing. Perfect for exhibitions, showrooms, and high-end retail environments.</p>`,
    specs: [['Material','Dye-sublimation printed polyester fabric'],['Frame','Lightweight aluminium snap frame'],['Finish','Seamless, vibrant full-colour print'],['Min. Order','1 pcs']],
    faq: [
      {q:'Is the fabric washable?',a:'Yes, the fabric can be hand-washed and is reusable.'},
      {q:'Does it come with a frame?',a:'Yes, all fabric displays include an aluminium snap frame.'},
    ],
    options: [
      {id:'size', label:'SIZE',      choices:['85cm x 200cm','100cm x 200cm','120cm x 200cm','150cm x 200cm','200cm x 200cm']},
      {id:'shape',label:'SHAPE',     choices:['Rectangle','Arch Top','Wave']},
      {id:'base', label:'BASE TYPE', choices:['Cross Base (Standard)','Water Base (+$20)','No Base (Wall Mount)']},
    ],
    quantities: [1,2,3,5,10],
    pricingMatrix: {1:[239.80,210,185],2:[450,395,345],3:[640,560,490],5:[990,868,758],10:[1800,1575,1380]},
    origMatrix:    {1:[252.50,221,195],2:[474,416,363],3:[674,590,516],5:[1042,913,798],10:[1895,1658,1453]},
    related: ['roll-up-banners','vinyl-banners','popup-display','foam-board'],
  },

  'vinyl-banners': {
    name: 'Vinyl Banners',
    category: 'Displays & Banners',
    img: 'img/services/banner.jpg',
    basePrice: 45, origPrice: null, discount: 0,
    description: `<p>Vinyl banners are durable, weather-resistant, and ideal for outdoor advertising, events, and promotions. Available in custom sizes with hemmed edges and grommets for easy hanging.</p>`,
    specs: [['Material','440gsm PVC Vinyl'],['Finish','Gloss or Matte'],['Edges','Hemmed with metal grommets'],['Min. Order','1 pcs']],
    faq: [
      {q:'Are vinyl banners suitable for outdoor use?',a:'Yes, our vinyl banners are UV-resistant and weatherproof.'},
    ],
    options: [
      {id:'size',    label:'SIZE',     choices:['1m x 2m','1m x 3m','2m x 3m','1.5m x 3m','Custom Size']},
      {id:'material',label:'MATERIAL', choices:['440gsm PVC (Standard)','510gsm PVC (Heavy Duty)','Mesh PVC (Wind-Resistant)']},
      {id:'finish',  label:'FINISH',   choices:['Gloss','Matte']},
      {id:'grommets',label:'GROMMETS', choices:['Grommets Every 50cm','Grommets Every 100cm','No Grommets']},
    ],
    quantities: [1,2,3,5,10,20],
    pricingMatrix: {1:[45,38,32],2:[82,69,58],3:[116,98,82],5:[180,152,127],10:[330,278,232],20:[600,505,422]},
    origMatrix:    {1:[null,null,null],2:[null,null,null],3:[null,null,null],5:[null,null,null],10:[null,null,null],20:[null,null,null]},
    related: ['roll-up-banners','fabric-displays','foam-board','popup-display'],
  },

  'popup-display': {
    name: 'Pop-Up Display',
    category: 'Displays & Banners',
    img: 'img/services/banner.jpg',
    basePrice: 440, origPrice: null, discount: 0,
    description: `<p>Pop-up displays create a large, eye-catching backdrop for exhibitions, trade shows, and corporate events. Easy to assemble and come with a carry case.</p>`,
    specs: [['Sizes','3x3 panels, 3x4 panels, 3x5 panels'],['Material','Magnetic frame with fabric graphic'],['Setup','Tool-free, under 5 minutes'],['Min. Order','1 pcs']],
    faq: [
      {q:'How long does setup take?',a:'Pop-up displays can be set up in under 5 minutes without any tools.'},
    ],
    options: [
      {id:'size',   label:'SIZE',         choices:['3x3 Panels (2.3m wide)','3x4 Panels (2.3m wide, taller)','3x5 Panels (3m wide)']},
      {id:'graphic',label:'GRAPHIC TYPE', choices:['Fabric Graphic (Premium)','PVC Graphic (Standard)']},
      {id:'lights', label:'LIGHTING',     choices:['No Lights','LED Spotlights (+$45)','LED Strip Lights (+$65)']},
    ],
    quantities: [1,2,3,5],
    pricingMatrix: {1:[440,395,360],2:[840,755,688],3:[1200,1080,984],5:[1850,1665,1518]},
    origMatrix:    {1:[null,null,null],2:[null,null,null],3:[null,null,null],5:[null,null,null]},
    related: ['fabric-displays','roll-up-banners','vinyl-banners','foam-board'],
  },

  'postcards': {
    name: 'Postcards',
    category: 'Stationery, Cards & Invites',
    img: 'img/services/post_card.jpg',
    basePrice: 11.53, origPrice: null, discount: 0,
    description: `<p>Postcards are a versatile marketing tool for direct mail campaigns, thank-you cards, promotional mailers, and event invitations. Printed on thick, premium card stock.</p>`,
    specs: [['Sizes','A6 (105x148mm), A5 (148x210mm), DL (99x210mm)'],['Paper','300gsm, 350gsm Art Card'],['Sides','Single Side, Double Side'],['Min. Order','25 pcs']],
    faq: [
      {q:'Can postcards be used for direct mail?',a:'Yes, our postcards meet Singapore Post size and weight requirements for direct mail.'},
    ],
    options: [
      {id:'size',  label:'SIZE',         choices:['A6 (105x148mm)','A5 (148x210mm)','DL (99x210mm)','Square (148x148mm)']},
      {id:'sides', label:'SIDE OF PRINT',choices:['Single Side','Double Side (+$3)']},
      {id:'paper', label:'PAPER STOCK',  choices:['300gsm Gloss Art Card','350gsm Premium Art Card','300gsm Matte Art Card']},
      {id:'finish',label:'FINISH',       choices:['None','Gloss Lamination','Matte Lamination']},
    ],
    quantities: [25,50,100,250,500,1000],
    pricingMatrix: {25:[11.53,9.50,8.00],50:[18,15,12.50],100:[28,23,19],250:[55,45,38],500:[90,75,63],1000:[155,129,108]},
    origMatrix:    {25:[null,null,null],50:[null,null,null],100:[null,null,null],250:[null,null,null],500:[null,null,null],1000:[null,null,null]},
    related: ['name-cards','flyers','greeting-cards','stickers'],
  },

  'greeting-cards': {
    name: 'Greeting & Invitation Cards',
    category: 'Stationery, Cards & Invites',
    img: 'img/services/post_card.jpg',
    basePrice: 8.65, origPrice: 26.15, discount: 66,
    description: `<p>Premium greeting cards and invitations for weddings, corporate events, birthdays, and festive occasions. Printed on luxurious card stock with optional foil stamping and embossing.</p>`,
    specs: [['Sizes','A6, A5, Square, DL'],['Paper','350gsm, 400gsm Premium Card'],['Finish','Gloss, Matte, Soft Touch, Foil'],['Min. Order','25 pcs']],
    faq: [
      {q:'Can I get foil stamping on my cards?',a:'Yes, gold and silver foil stamping is available as an add-on.'},
    ],
    options: [
      {id:'size',    label:'SIZE',         choices:['A6 (105x148mm)','A5 (148x210mm)','Square (148x148mm)','DL (99x210mm)']},
      {id:'paper',   label:'PAPER STOCK',  choices:['350gsm Premium Card','400gsm Ultra Thick Card','300gsm Textured Card']},
      {id:'finish',  label:'FINISH',       choices:['Matte Lamination','Gloss Lamination','Soft Touch Matte','Gold Foil (+$15)','Silver Foil (+$15)']},
      {id:'envelope',label:'ENVELOPE',     choices:['No Envelope','White Envelope (+$0.50/pc)','Kraft Envelope (+$0.80/pc)']},
    ],
    quantities: [25,50,100,250,500],
    pricingMatrix: {25:[8.65,7.20,6.00],50:[14,11.50,9.50],100:[22,18,15],250:[42,35,29],500:[70,58,48]},
    origMatrix:    {25:[26.15,21.80,18.15],50:[42,35,29],100:[66,55,45],250:[127,106,88],500:[212,177,147]},
    related: ['postcards','name-cards','stickers','flyers'],
  },

  'gift-vouchers': {
    name: 'Gift Vouchers & Coupons',
    category: 'Stationery, Cards & Invites',
    img: 'img/services/post_card.jpg',
    basePrice: 24.46, origPrice: null, discount: 0,
    description: `<p>Custom gift vouchers and coupons are a powerful tool to drive sales and customer loyalty. Printed on premium card stock with optional security features.</p>`,
    specs: [['Sizes','DL (99x210mm), A6, Custom'],['Paper','300gsm, 350gsm Art Card'],['Features','Serial numbering, Perforation, Scratch-off'],['Min. Order','100 pcs']],
    faq: [
      {q:'Can vouchers have unique serial numbers?',a:'Yes, we offer sequential serial numbering as an add-on.'},
    ],
    options: [
      {id:'size',  label:'SIZE',             choices:['DL (99x210mm)','A6 (105x148mm)','Credit Card Size (85x54mm)']},
      {id:'paper', label:'PAPER STOCK',      choices:['300gsm Gloss Art Card','350gsm Premium Art Card']},
      {id:'extras',label:'SPECIAL FEATURES', choices:['None','Serial Numbering (+$8)','Perforation (+$5)','Scratch-Off Coating (+$12)']},
    ],
    quantities: [100,250,500,1000,2000],
    pricingMatrix: {100:[24.46,20,17],250:[45,37,31],500:[72,60,50],1000:[120,100,83],2000:[200,167,139]},
    origMatrix:    {100:[null,null,null],250:[null,null,null],500:[null,null,null],1000:[null,null,null],2000:[null,null,null]},
    related: ['postcards','stickers','name-cards','flyers'],
  },

  'tshirts': {
    name: 'T-Shirts & Apparel',
    category: 'Promo & Giveaways',
    img: 'img/services/tshirt_printing.jpg',
    basePrice: 18, origPrice: null, discount: 0,
    description: `<p>Custom printed t-shirts and apparel for corporate events, team uniforms, promotions, and merchandise. We offer screen printing, heat transfer, and embroidery options.</p>`,
    specs: [['Fabric','100% Cotton, Polyester, Cotton-Poly Blend'],['Print Method','Screen Print, Heat Transfer, Embroidery'],['Sizes','XS-5XL'],['Min. Order','10 pcs']],
    faq: [
      {q:'What is the minimum order?',a:'Minimum order is 10 pcs for screen printing.'},
      {q:'Can I mix sizes in one order?',a:'Yes, you can mix sizes within the same order.'},
    ],
    options: [
      {id:'style', label:'STYLE',          choices:['Round Neck T-Shirt','Polo Shirt','Hoodie','Singlet']},
      {id:'fabric',label:'FABRIC',         choices:['100% Cotton (180gsm)','Polyester Dri-Fit','Cotton-Poly Blend (50/50)']},
      {id:'print', label:'PRINT METHOD',   choices:['Screen Print (1 colour)','Screen Print (Full Colour)','Heat Transfer','Embroidery (+$3/pc)']},
      {id:'sides', label:'PRINT LOCATION', choices:['Front Only','Back Only','Front & Back (+$5/pc)','Left Chest Only']},
    ],
    quantities: [10,20,50,100,200,500],
    pricingMatrix: {10:[18,16,14],20:[32,28,24],50:[70,62,54],100:[120,106,92],200:[210,185,162],500:[480,424,371]},
    origMatrix:    {10:[null,null,null],20:[null,null,null],50:[null,null,null],100:[null,null,null],200:[null,null,null],500:[null,null,null]},
    related: ['name-cards','stickers','gift-vouchers','corporate-gifts'],
  },

  'corporate-gifts': {
    name: 'Corporate Gifts',
    category: 'Promo & Giveaways',
    img: 'img/services/corporate_gifts.jpg',
    basePrice: 12, origPrice: null, discount: 0,
    description: `<p>Branded corporate gifts and promotional merchandise to strengthen your brand and delight clients. From pens and notebooks to tote bags and umbrellas.</p>`,
    specs: [['Items','Pens, Notebooks, Tote Bags, Umbrellas, Mugs, USB Drives'],['Branding','Screen Print, Laser Engraving, Embroidery'],['Min. Order','50 pcs']],
    faq: [
      {q:'Can I see a sample before ordering?',a:'Yes, samples are available for most items. Please contact us for sample requests.'},
    ],
    options: [
      {id:'item',    label:'ITEM TYPE',       choices:['Ballpoint Pen','Notebook (A5)','Tote Bag','Umbrella','Ceramic Mug','USB Drive (8GB)']},
      {id:'branding',label:'BRANDING METHOD', choices:['Screen Print (1 colour)','Full Colour Print','Laser Engraving','Embroidery']},
    ],
    quantities: [50,100,250,500,1000],
    pricingMatrix: {50:[12,10,9],100:[20,17,14],250:[42,35,29],500:[75,63,52],1000:[130,109,90]},
    origMatrix:    {50:[null,null,null],100:[null,null,null],250:[null,null,null],500:[null,null,null],1000:[null,null,null]},
    related: ['tshirts','stickers','name-cards','gift-vouchers'],
  },

  'envelopes': {
    name: 'Envelopes',
    category: 'Stationery, Cards & Invites',
    img: 'img/services/envelope.jpg',
    basePrice: 15, origPrice: null, discount: 0,
    description: `<p>Custom printed envelopes for corporate correspondence, direct mail, and event invitations. Available in a range of sizes with full-colour or single-colour printing.</p>`,
    specs: [['Sizes','DL, C5, C4, Square'],['Paper','100gsm, 120gsm'],['Printing','Full Colour, Single Colour'],['Min. Order','100 pcs']],
    faq: [
      {q:'Can I print on both sides?',a:'Yes, we can print on the front flap and back of envelopes.'},
    ],
    options: [
      {id:'size', label:'SIZE',  choices:['DL (110x220mm)','C5 (162x229mm)','C4 (229x324mm)','Square (160x160mm)']},
      {id:'paper',label:'PAPER', choices:['100gsm White','120gsm White','100gsm Kraft Brown']},
      {id:'print',label:'PRINT', choices:['Full Colour (Outside)','Single Colour (Outside)','Full Colour (Inside & Outside)']},
    ],
    quantities: [100,250,500,1000,2500,5000],
    pricingMatrix: {100:[15,12.50,10.50],250:[28,23,19],500:[45,37,31],1000:[72,60,50],2500:[150,125,104],5000:[260,217,181]},
    origMatrix:    {100:[null,null,null],250:[null,null,null],500:[null,null,null],1000:[null,null,null],2500:[null,null,null],5000:[null,null,null]},
    related: ['postcards','flyers','name-cards','greeting-cards'],
  },

  'foam-board': {
    name: 'Foam Board',
    category: 'Signages',
    img: 'img/services/banner.jpg',
    basePrice: 28, origPrice: null, discount: 0,
    description: `<p>Foam board prints are lightweight, rigid display boards ideal for exhibitions, retail displays, directional signage, and presentations.</p>`,
    specs: [['Sizes','A3, A2, A1, A0, Custom'],['Thickness','3mm, 5mm, 10mm'],['Material','Foam core with paper or PVC surface'],['Min. Order','1 pcs']],
    faq: [
      {q:'Can foam boards be mounted on walls?',a:'Yes, foam boards can be mounted with double-sided tape or Velcro strips.'},
    ],
    options: [
      {id:'size',     label:'SIZE',      choices:['A3 (297x420mm)','A2 (420x594mm)','A1 (594x841mm)','A0 (841x1189mm)','Custom Size']},
      {id:'thickness',label:'THICKNESS', choices:['3mm','5mm','10mm']},
      {id:'surface',  label:'SURFACE',   choices:['Gloss Paper','Matte Paper','PVC (Waterproof)']},
    ],
    quantities: [1,2,5,10,20,50],
    pricingMatrix: {1:[28,24,20],2:[50,43,36],5:[110,94,79],10:[195,167,140],20:[350,300,251],50:[780,668,559]},
    origMatrix:    {1:[null,null,null],2:[null,null,null],5:[null,null,null],10:[null,null,null],20:[null,null,null],50:[null,null,null]},
    related: ['vinyl-banners','roll-up-banners','fabric-displays','popup-display'],
  },

  'brochures': {
    name: 'Brochures',
    category: 'Marketing & Print Advertising',
    img: 'img/services/booklet.jpg',
    basePrice: 35, origPrice: null, discount: 0,
    description: `<p>Professional brochures for marketing, product showcases, and company profiles. Available in tri-fold, bi-fold, and z-fold formats on premium art paper.</p>`,
    specs: [['Sizes','A4, A5, DL'],['Folds','Tri-fold, Bi-fold, Z-fold, Gate-fold'],['Paper','128gsm, 150gsm, 170gsm Art Paper'],['Min. Order','100 pcs']],
    faq: [
      {q:'What fold types are available?',a:'We offer tri-fold, bi-fold, z-fold, and gate-fold options.'},
    ],
    options: [
      {id:'size',  label:'SIZE',       choices:['A4 (210x297mm)','A5 (148x210mm)','DL (99x210mm)']},
      {id:'fold',  label:'FOLD TYPE',  choices:['Tri-fold (6 panels)','Bi-fold (4 panels)','Z-fold (6 panels)','Gate-fold (6 panels)']},
      {id:'paper', label:'PAPER STOCK',choices:['128gsm Gloss Art Paper','150gsm Gloss Art Paper','170gsm Matte Art Paper']},
      {id:'finish',label:'FINISH',     choices:['None','Gloss Lamination (Cover)','Matte Lamination (Cover)']},
    ],
    quantities: [100,250,500,1000,2000,5000],
    pricingMatrix: {100:[35,28,23],250:[62,50,41],500:[100,80,66],1000:[165,132,109],2000:[280,224,185],5000:[580,464,383]},
    origMatrix:    {100:[null,null,null],250:[null,null,null],500:[null,null,null],1000:[null,null,null],2000:[null,null,null],5000:[null,null,null]},
    related: ['flyers','booklets','name-cards','postcards'],
  },

};

/* ═══════════════════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════════════════ */
let currentProduct = null;
let selectedOptions = {};
let selectedCell = null; // { qty, colIdx }
let designChoice = 'upload';
let customQties = [];

/* ═══════════════════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id') || 'name-cards';
  loadProduct(id);

  // Delivery column dates
  DELIVERY_COLS.forEach((col, i) => {
    const el = document.getElementById(`col-date-${i}`);
    if (el) el.textContent = col.label;
  });

  // Product details tabs
  document.querySelectorAll('.prod-details-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.prod-details-tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.prod-details-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(`dtab-${btn.dataset.dtab}`).classList.add('active');
    });
  });

  // Hero tabs
  document.querySelectorAll('.prod-hero-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.prod-hero-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.section;
      if (target === 'configurator') {
        document.getElementById('section-configurator').scrollIntoView({ behavior: 'smooth' });
      } else if (target === 'details') {
        document.getElementById('section-details').scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Add to cart
  document.getElementById('btn-add-cart').addEventListener('click', addToCart);
  document.getElementById('btn-whatsapp').addEventListener('click', orderWhatsApp);

  // Cart count from localStorage
  const count = parseInt(localStorage.getItem('ppsg_cart') || '0');
  document.getElementById('cart-count').textContent = count;
});

/* ═══════════════════════════════════════════════════════════════
   LOAD PRODUCT
═══════════════════════════════════════════════════════════════ */
function loadProduct(id) {
  const p = PRODUCTS[id];
  if (!p) {
    document.body.innerHTML = '<div style="padding:60px;text-align:center;font-size:18px">Product not found. <a href="index.html">Go back</a></div>';
    return;
  }
  currentProduct = p;
  selectedOptions = {};
  selectedCell = null;
  customQties = [];

  document.title = `${p.name} — Print Pro Singapore`;
  document.getElementById('page-title').textContent = `${p.name} — Print Pro Singapore`;
  document.getElementById('bc-cat').textContent = p.category;
  document.getElementById('bc-name').textContent = p.name;
  document.getElementById('hero-title').textContent = p.name;
  document.getElementById('hero-img').src = p.img;
  document.getElementById('hero-img').alt = p.name;
  document.getElementById('hero-img').onerror = function() { this.src = 'img/services/name_card.jpg'; };

  updateHeroPrice();

  const pdBadge = document.getElementById('hero-pricedrop');
  pdBadge.style.display = p.discount > 0 ? 'block' : 'none';

  document.getElementById('options-product-title').textContent = p.name;
  buildOptions(p);
  renderPricingTable();
  document.getElementById('prod-description').innerHTML = buildDescription(p);
  document.getElementById('prod-faq').innerHTML = buildFAQ(p);
  buildRelated(p);
  showEmptyOrderSummary();
}

function updateHeroPrice() {
  const p = currentProduct;
  const qty = p.quantities[0];
  const price = p.pricingMatrix[qty][2];
  const orig = p.origMatrix[qty][2];
  document.getElementById('hero-price').textContent = price.toFixed(2);
  document.getElementById('hero-unit').textContent = `Per ${qty} pcs`;
  if (orig && orig > price) {
    document.getElementById('hero-orig').style.display = 'inline';
    document.getElementById('hero-orig').textContent = `SGD ${orig.toFixed(2)}`;
    document.getElementById('hero-off').style.display = 'inline';
    document.getElementById('hero-off').textContent = `${p.discount}% off`;
  } else {
    document.getElementById('hero-orig').style.display = 'none';
    document.getElementById('hero-off').style.display = 'none';
  }
}

/* ═══════════════════════════════════════════════════════════════
   BUILD OPTIONS (Step 2)
═══════════════════════════════════════════════════════════════ */
function buildOptions(p) {
  const container = document.getElementById('options-container');
  container.innerHTML = '';
  p.options.forEach(opt => {
    selectedOptions[opt.id] = opt.choices[0];
    const group = document.createElement('div');
    group.className = 'opt-group';
    group.innerHTML = `
      <div class="opt-group-label">${opt.label}</div>
      <div class="opt-select-wrap">
        <select class="opt-select" data-opt="${opt.id}" onchange="onOptionChange('${opt.id}', this.value)">
          ${opt.choices.map(c => `<option value="${c}">${c}</option>`).join('')}
        </select>
      </div>
    `;
    container.appendChild(group);
  });
}

function onOptionChange(optId, value) {
  selectedOptions[optId] = value;
  updateOrderSummary();
}

/* ═══════════════════════════════════════════════════════════════
   DESIGN CHOICE (Step 1)
═══════════════════════════════════════════════════════════════ */
function selectDesign(choice) {
  designChoice = choice;
  document.querySelectorAll('.design-opt').forEach(el => el.classList.remove('active'));
  document.getElementById(`opt-${choice}`).classList.add('active');
  const dsRow = document.getElementById('os-design-row');
  if (dsRow) dsRow.style.display = choice === 'design' ? 'flex' : 'none';
  updateOrderSummary();
}

/* ═══════════════════════════════════════════════════════════════
   PRICING TABLE (Step 3)
═══════════════════════════════════════════════════════════════ */
function renderPricingTable() {
  const p = currentProduct;
  if (!p) return;
  const tbody = document.getElementById('pricing-tbody');
  tbody.innerHTML = '';

  const allQties = [...p.quantities, ...customQties].sort((a, b) => a - b);

  allQties.forEach(qty => {
    const prices = p.pricingMatrix[qty] || [null, null, null];
    const origs  = p.origMatrix[qty]   || [null, null, null];
    const tr = document.createElement('tr');
    tr.innerHTML = `<td class="td-qty">${qty.toLocaleString()} pcs</td>` +
      [0, 1, 2].map(ci => {
        let price = prices[ci];
        let orig  = origs[ci];
        if (price == null) return `<td class="price-cell"><div class="price-cell-inner" style="opacity:.4;cursor:default">N/A</div></td>`;
        if (gstOn) { price = price * 1.09; if (orig) orig = orig * 1.09; }
        const isSelected = selectedCell && selectedCell.qty === qty && selectedCell.colIdx === ci;
        const perPiece = (price / qty).toFixed(4);
        const hasDiscount = orig && orig > price;
        return `<td class="price-cell" onclick="selectPriceCell(${qty}, ${ci})">
          <div class="price-cell-inner${isSelected ? ' selected' : ''}">
            ${hasDiscount ? `<span class="pc-orig">$${orig.toFixed(2)}</span>` : ''}
            <span class="pc-price${hasDiscount ? ' has-discount' : ''}">$${price.toFixed(2)}</span>
            <span class="pc-per">$${perPiece} per piece</span>
          </div>
        </td>`;
      }).join('');
    tbody.appendChild(tr);
  });
}

function selectPriceCell(qty, colIdx) {
  selectedCell = { qty, colIdx };
  renderPricingTable();
  updateOrderSummary();
  if (window.innerWidth < 960) {
    document.querySelector('.order-summary').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

/* ═══════════════════════════════════════════════════════════════
   ORDER SUMMARY
═══════════════════════════════════════════════════════════════ */
function showEmptyOrderSummary() {
  document.getElementById('os-empty').style.display = 'block';
  document.getElementById('os-details').style.display = 'none';
  document.getElementById('btn-add-cart').disabled = true;
}

function updateOrderSummary() {
  if (!selectedCell) { showEmptyOrderSummary(); return; }
  const p = currentProduct;
  const { qty, colIdx } = selectedCell;
  let price = p.pricingMatrix[qty][colIdx];
  let orig  = p.origMatrix[qty][colIdx];
  if (price == null) { showEmptyOrderSummary(); return; }
  if (gstOn) { price = price * 1.09; if (orig) orig = orig * 1.09; }

  let designFee = 0;
  if (designChoice === 'design') designFee = 45;

  const total = price + designFee;
  const perPiece = (price / qty).toFixed(4);
  const saving = (orig && orig > price) ? (orig - price) : 0;

  document.getElementById('os-empty').style.display = 'none';
  document.getElementById('os-details').style.display = 'block';
  document.getElementById('os-product-name').textContent = p.name;

  const optSummary = Object.values(selectedOptions).join(', ');
  document.getElementById('os-options').textContent = optSummary || '—';
  document.getElementById('os-qty').textContent = `${qty.toLocaleString()} pcs`;
  document.getElementById('os-delivery').textContent = DELIVERY_COLS[colIdx].label;

  const dsRow = document.getElementById('os-design-row');
  dsRow.style.display = designChoice === 'design' ? 'flex' : 'none';

  document.getElementById('os-total').textContent = `SGD ${total.toFixed(2)}`;
  document.getElementById('os-per').textContent = `SGD ${perPiece} per piece`;

  if (saving > 0.01) {
    document.getElementById('os-saving').style.display = 'flex';
    document.getElementById('os-saving-text').textContent = `You save SGD ${saving.toFixed(2)}!`;
  } else {
    document.getElementById('os-saving').style.display = 'none';
  }

  document.getElementById('btn-add-cart').disabled = false;
}

/* ═══════════════════════════════════════════════════════════════
   ADD TO CART
═══════════════════════════════════════════════════════════════ */
function addToCart() {
  if (!selectedCell) return;
  const count = parseInt(localStorage.getItem('ppsg_cart') || '0') + 1;
  localStorage.setItem('ppsg_cart', count);
  document.getElementById('cart-count').textContent = count;

  const btn = document.getElementById('btn-add-cart');
  const orig = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-check"></i> Added to Cart!';
  btn.style.background = '#16a34a';
  setTimeout(() => {
    btn.innerHTML = orig;
    btn.style.background = '';
  }, 2000);
}

/* ═══════════════════════════════════════════════════════════════
   WHATSAPP ORDER
═══════════════════════════════════════════════════════════════ */
function orderWhatsApp() {
  if (!selectedCell) return;
  const p = currentProduct;
  const { qty, colIdx } = selectedCell;
  const price = p.pricingMatrix[qty][colIdx];
  const optLines = Object.entries(selectedOptions).map(([k, v]) => `• ${k}: ${v}`).join('\n');
  const msg = `Hello Print Pro SG! I'd like to order:\n\n*${p.name}*\n${optLines}\n• Quantity: ${qty} pcs\n• Delivery by: ${DELIVERY_COLS[colIdx].label}\n• Design: ${designChoice === 'upload' ? 'I will upload my own design' : 'Please design for me'}\n\n*Total: SGD ${price.toFixed(2)}*\n\nPlease confirm availability and payment details. Thank you!`;
  window.open(`https://wa.me/6598751606?text=${encodeURIComponent(msg)}`, '_blank');
}

/* ═══════════════════════════════════════════════════════════════
   CUSTOM QTY MODAL
═══════════════════════════════════════════════════════════════ */
function openCustomQty() {
  document.getElementById('custom-qty-modal').classList.add('open');
  document.getElementById('custom-qty-input').focus();
}
function closeCustomQty() {
  document.getElementById('custom-qty-modal').classList.remove('open');
}
function confirmCustomQty() {
  const val = parseInt(document.getElementById('custom-qty-input').value);
  if (!val || val < 1) { alert('Please enter a valid quantity.'); return; }
  const p = currentProduct;
  if (!customQties.includes(val) && !p.quantities.includes(val)) {
    customQties.push(val);
    const sortedQties = [...p.quantities].sort((a, b) => a - b);
    let nearestQty = sortedQties[0];
    for (const q of sortedQties) { if (q <= val) nearestQty = q; }
    const factor = val / nearestQty;
    p.pricingMatrix[val] = p.pricingMatrix[nearestQty].map(pr => parseFloat((pr * factor * 0.92).toFixed(2)));
    p.origMatrix[val]    = p.origMatrix[nearestQty].map(pr => pr ? parseFloat((pr * factor * 0.92).toFixed(2)) : null);
  }
  closeCustomQty();
  renderPricingTable();
}
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('custom-qty-modal');
  if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeCustomQty(); });
});

/* ═══════════════════════════════════════════════════════════════
   DESCRIPTION & FAQ HTML BUILDERS
═══════════════════════════════════════════════════════════════ */
function buildDescription(p) {
  let html = p.description || '';
  if (p.specs && p.specs.length) {
    html += `<table class="specs-table" style="margin-top:16px">`;
    p.specs.forEach(([label, val]) => {
      html += `<tr><td>${label}</td><td>${val}</td></tr>`;
    });
    html += `</table>`;
  }
  return html;
}

function buildFAQ(p) {
  if (!p.faq || !p.faq.length) return '<p>No FAQ available for this product.</p>';
  return p.faq.map(item => `
    <div style="margin-bottom:16px">
      <div style="font-size:14px;font-weight:700;color:var(--ink1);margin-bottom:4px">Q: ${item.q}</div>
      <div style="font-size:13px;color:var(--ink2);line-height:1.6">A: ${item.a}</div>
    </div>
  `).join('');
}

/* ═══════════════════════════════════════════════════════════════
   RELATED PRODUCTS
═══════════════════════════════════════════════════════════════ */
function buildRelated(p) {
  const grid = document.getElementById('related-grid');
  grid.innerHTML = '';
  (p.related || []).slice(0, 4).forEach(rid => {
    const rp = PRODUCTS[rid];
    if (!rp) return;
    const card = document.createElement('div');
    card.className = 'related-card';
    card.onclick = () => { window.location.href = `product.html?id=${rid}`; };
    const minPrice = rp.pricingMatrix[rp.quantities[0]][2];
    const origPrice = rp.origMatrix[rp.quantities[0]][2];
    card.innerHTML = `
      <img class="related-card-img" src="${rp.img}" alt="${rp.name}" onerror="this.src='img/services/name_card.jpg'" />
      <div class="related-card-body">
        <div class="related-card-name">${rp.name}</div>
        <div>
          <span class="related-card-price">SGD ${minPrice.toFixed(2)}</span>
          ${origPrice && origPrice > minPrice ? `<span class="related-card-orig" style="margin-left:6px">SGD ${origPrice.toFixed(2)}</span>` : ''}
        </div>
      </div>
      <a href="product.html?id=${rid}" class="related-card-cta">Configure &amp; Get Price</a>
    `;
    grid.appendChild(card);
  });
}
