# Maintainer: Marco Fontana <ciabadiale@gmail.com>
pkgname=subito-it-scraper
pkgver=1
pkgrel=1
pkgdesc="Item tracker for subito.it website"
arch=('x86_64')
license=('GPL3')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-regex')
source=("file://subito-it-scraper.py")
provides=("${pkgname}")
conflicts=("${pkgname}")
sha256sums=('e07a5711e5824c5e22b1f47d20b1b24b5b8ae19a736dd07597fb9fc34a85d088')

package() {
    cd "${srcdir}"
    install -D "${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
