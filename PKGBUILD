# Maintainer: Marco Fontana <ciabadiale@gmail.com>
pkgname=subito-it-scraper
pkgver=0.3
pkgrel=1
pkgdesc='Item tracker for subito.it website'
arch=('x86_64')
license=('GPL3')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-regex')
source=('file://subito-it-scraper.py')
provides=("${pkgname}")
conflicts=("${pkgname}")
sha256sums=('f9df9efd188bf76e5cf5f09d29da15d7d4fb93f2b406c2a2fba6a710fb11ab02')

package() {
    cd "${srcdir}"
    install -D "${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
