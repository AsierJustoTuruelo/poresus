if args.imagemetadata:
    # Ejecutar Image Metadata scanner
    image_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
    image_metadata_scanner = OnionImageScanner(urls)
    image_metadata_results = image_metadata_scanner.scan_images()

    # Convertir datos no serializables a un formato adecuado
    if isinstance(image_metadata_results, bytes):
        # Ejemplo: Decodificar bytes a cadena UTF-8 si es texto
        image_metadata_results = image_metadata_results.decode('utf-8')

    results["Image Metadata Results"] = {
        "Image Metadata Results": image_metadata_results
    }
