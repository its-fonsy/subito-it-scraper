# Maintainer: Marco Fontana <ciabadiale@gmail.com>
pkgname=subito-it-scraper
pkgver=0.4
pkgrel=1
pkgdesc='Item tracker for subito.it website'
arch=('x86_64')
license=('GPL3')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-regex')
source=('file://subito-it-scraper.py')
provides=("${pkgname}")
conflicts=("${pkgname}")
sha256sums=('967b2ad1c98462e4f84807d83c92559d155d9290937dafb18799596f9aae4a84')

package() {
    cd "${srcdir}"
    install -D "${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
