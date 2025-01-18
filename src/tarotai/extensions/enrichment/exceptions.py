class EnrichmentError(Exception):
    """Base class for enrichment-related errors"""
    pass

class GoldenDawnProcessingError(EnrichmentError):
    """Errors specific to Golden Dawn knowledge processing"""
    pass

class ImageProcessingError(EnrichmentError):
    """Errors related to image processing"""
    pass

class HistoryProcessingError(EnrichmentError):
    """Errors related to reading history processing"""
    pass
