import unittest

from deptools.register import packages_from_files, Package, is_linux_resource, get_category, get_md5_content


class TestRegister(unittest.TestCase):
    def test_packages_from_file(self):
        packages = packages_from_files(
            ['path/to/installer/ats-sdk-rpm_v7.5.0.zip', '/path/to/installer/ATS-SDK-ReleaseNotes.html'])
        self.assertEqual(packages, [
            Package(os='Linux (.rpm)',
                    product_id='1018',
                    installer='ats-sdk-rpm_v7.5.0.zip',
                    readme='ATS-SDK-ReleaseNotes.html',
                    name='ATS-SDK',
                    arch='x86_64',
                    category='software',
                    name_french='ATS-SDK')
        ])
        packages = packages_from_files(
            ['/path/to/installer/drivers-ats9352-dkms_7.3.1_arm64.deb', '/path/to/installer/ATS9352_Driver_V7.3.1_Readme.html'])
        self.assertEqual(packages, [
            Package(os='Linux (.deb)',
                    product_id='1036',
                    installer='drivers-ats9352-dkms_7.3.1_arm64.deb',
                    readme='ATS9352_Driver_V7.3.1_Readme.html',
                    name='ATS9352 arm64 driver for Linux',
                    arch='arm64',
                    category='driver',
                    name_french='Pilotes ATS9352 arm64 pour Linux'),
            Package(os='Linux (.deb)',
                    product_id='1045',
                    installer='drivers-ats9352-dkms_7.3.1_arm64.deb',
                    readme='ATS9352_Driver_V7.3.1_Readme.html',
                    name='ATS9352 arm64 driver for Linux',
                    arch='arm64',
                    category='driver',
                    name_french='Pilotes ATS9352 arm64 pour Linux')
        ])
        package = Package(os='Linux (.deb)',
                        product_id='-1',
                        installer='',
                        readme='',
                        name='Libats library [REQUIRED]',
                        arch='x86_64',
                        category='',
                        name_french='')
        self.assertEqual(is_linux_resource(package), 1)
        package = Package(os='Windows',
                        product_id='',
                        installer='',
                        readme='',
                        name='Libats library [REQUIRED]',
                        arch='',
                        category='',
                        name_french='')
        self.assertEqual(is_linux_resource(package), 0)
        self.assertEqual(get_category('ATS9352'), 'driver')
        self.assertEqual(get_category('libats'), 'driver')
        self.assertEqual(get_category('fwupdater-cli'), 'utility')
        self.assertEqual(get_md5_content('https://alazarblob1.blob.core.windows.net/licensed/ats-sdk-windows_v7.5.0.zip'), "bytearray(b'\\x03\\xe7\\xd0h\\xc2EG\\xd0\\x95\\x0c\\x8fO\\x86=+\\xc1')")
        self.assertEqual(get_md5_content('https://alazarblob1.blob.core.windows.net/packages/ATS9352_Driver_V7.3.0.exe'), 'bytearray(b"\\xd2Uu@\\x83\\xf7\\x83P\\x8ar\\xf5\\x07\\xb9\\\'\\xa4\\x04")')
        


if __name__ == "__main__":
    unittest.main()
