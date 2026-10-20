// Tüm oyunlar burada. Yeni oyun eklemek için listeye bir kayıt eklemen yeterli.
// - id: adres çubuğunda görünen kısa ad (product.html?id=...)
// - logo: assets/ içindeki dosya, wide: yatay logolar için true
// - video: YouTube video ID'si (youtube.com/watch?v=XXXX → "XXXX"), boşsa "Video yakında" yazar
// - plans: fiyatlar; old = üstü çizili eski fiyat (yoksa sil), popular = öne çıkan plan
const PRODUCTS = [
  {
    id: 'r6', name: 'Rainbow Six Siege', logo: 'r6.svg', version: 'v2.4.1', video: '',
    description: 'Rainbow Six Siege için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺49' },
      { label: '1 Hafta', price: '₺199', old: '₺343', popular: true },
      { label: '1 Ay', price: '₺549', old: '₺1.470' },
    ],
  },
  {
    id: 'fivem', name: 'FiveM', logo: 'fivem.svg', version: 'v1.8.0', video: '',
    description: 'FiveM için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺39' },
      { label: '1 Hafta', price: '₺159', old: '₺273', popular: true },
      { label: '1 Ay', price: '₺449', old: '₺1.170' },
    ],
  },
  {
    id: 'squad', name: 'Squad', logo: 'squad.png', wide: true, version: 'v3.0.2', video: '',
    description: 'Squad için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺45' },
      { label: '1 Hafta', price: '₺179', old: '₺315', popular: true },
      { label: '1 Ay', price: '₺499', old: '₺1.350' },
    ],
  },
  {
    id: 'warzone', name: 'Call of Duty: Warzone', logo: 'warzone.svg', version: 'v1.2.0', video: '',
    description: 'Call of Duty: Warzone için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺55' },
      { label: '1 Hafta', price: '₺219', old: '₺385', popular: true },
      { label: '1 Ay', price: '₺599', old: '₺1.650' },
    ],
  },
  {
    id: 'arena', name: 'Arena Breakout: Infinite', logo: 'arena.png', wide: true, version: 'v1.0.4', video: '',
    description: 'Arena Breakout: Infinite için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺45' },
      { label: '1 Hafta', price: '₺179', old: '₺315', popular: true },
      { label: '1 Ay', price: '₺499', old: '₺1.350' },
    ],
  },
  {
    id: 'apex', name: 'Apex Legends', logo: 'apex.svg', version: 'v2.1.3', video: '',
    description: 'Apex Legends için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺55' },
      { label: '1 Hafta', price: '₺219', old: '₺385', popular: true },
      { label: '1 Ay', price: '₺599', old: '₺1.650' },
    ],
  },
  {
    id: 'metin2', name: 'Metin2', logo: 'metin2.png', wide: true, version: 'v1.0.0', video: '',
    description: 'Metin2 için hazırlanan paket. Kurulumu birkaç dakika sürer.',
    features: ['Kolay kurulum', 'Düzenli güncelleme', '7/24 destek'],
    plans: [
      { label: '1 Gün', price: '₺35' },
      { label: '1 Hafta', price: '₺139', old: '₺245', popular: true },
      { label: '1 Ay', price: '₺379', old: '₺1.050' },
    ],
  },
];

function logoHTML(p) {
  return `<span class="logo"><img${p.wide ? ' class="wide"' : ''} src="assets/${p.logo}" alt="${p.name} logosu"></span>`;
}
