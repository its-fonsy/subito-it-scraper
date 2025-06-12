# Maintainer: Marco Fontana <ciabadiale@gmail.com>
pkgname=subito-it-scraper
pkgver=0.1
pkgrel=1
pkgdesc='Item tracker for subito.it website'
arch=('x86_64')
license=('GPL3')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-regex')
source=('file://subito-it-scraper.py')
provides=("${pkgname}")
conflicts=("${pkgname}")
sha256sums=('045170043dd74463a2d6a963c2e2c4632fba62a18469ece0a857cc60e62b173c')

package() {
    cd "${srcdir}"
    install -D "${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
