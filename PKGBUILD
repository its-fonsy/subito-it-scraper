# Maintainer: Marco Fontana <ciabadiale@gmail.com>
pkgname=subito-it-scraper
pkgver=0.2
pkgrel=1
pkgdesc='Item tracker for subito.it website'
arch=('x86_64')
license=('GPL3')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-regex')
source=('file://subito-it-scraper.py')
provides=("${pkgname}")
conflicts=("${pkgname}")
sha256sums=('2e6408bdc363b6b438c1c57d5943de1b3c2d94ec707d354b74b640adeed86bbb')

package() {
    cd "${srcdir}"
    install -D "${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
