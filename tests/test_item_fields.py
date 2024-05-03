"""
Module Test Fields

This module contains test functions for different fields in the item object. Each test function
compares a specific field of the item with an expected value or condition.

Functions:
- test_field_ProductTitle(): Checks 'Product Title' field of the item.
- test_field_PublishDate(): Checks 'Publish Date' field of the item.
- test_field_Contact(): Checks 'Contact' field of the item.
- test_field_PublishLink(): Checks 'Publish Link' field of the item.
- test_field_ProductPrice(): Checks 'Product Price' field of the item.
- test_field_VendorLocation(): Checks 'Vendor Location' field of the item.
"""
from vacuum.Item import MainItem
from scrapy import Selector

html = """          <div class="listings-cards__list-item">
            <div
              class="listing-card listing-card--tab listing-card--has-content listing-card--highlight-placeholder"
            >
              <a
                href="https://www.test-site.com/annonce/centre-dappels-6056386"
                class="listing-card__inner"
                id="listing-6056386"
                data-t-listing=""
                data-t-listing_context="search"
                data-t-listing_id="6056386"
                data-t-listing_title="Centre d'Appels"
                data-t-listing_type="classified"
                data-t-listing_category_title="Emploi vente et commercial"
                data-t-listing_category_slug="emploi-vente-commercial"
                data-t-listing_slug="centre-dappels"
                data-t-listing_price="0"
                data-t-listing_currency=""
                data-t-listing_location_title="Liberte 6 extension"
                data-t-listing_source="ed_sn"
                data-t-listing_product_slugs="listing"
                data-uuid-ui="6056386"
                data-ei="not-set"
                ><div class="listing-card__aside">
                  <div class="listing-card__image">
                    <div
                      class="listing-card__image__inner-container"
                    >
                      <svg
                        class="i i-jobs listing-card__image__placeholder"
                        aria-hidden="true"
                      >
                        <use
                          xlink:href="https://www.test-site.com/assets/ed-site/icons/category.48eeb376.svg#jobs"
                        ></use>
                      </svg>
                      <div class="listing-card__image__inner">
                        <img
                          class="listing-card__image__resource vh-img"
                          alt="Centre d'Appels"
                          src="https://i.roamcdn.net/hz/ed/listing-thumb-224w/04b5375ca21184b4dde2027303d970a8/-/horizon-files-prod/ed/picture/qenq4ev9/73f70842ddaed70d34872e9cdcd9c424b2d87aaf.jpg"
                          loading="lazy"
                          srcset="
                            https://i.roamcdn.net/hz/ed/listing-thumb-112w/e467bb1653809cd0401f719ca176f5d3/-/horizon-files-prod/ed/picture/qenq4ev9/73f70842ddaed70d34872e9cdcd9c424b2d87aaf.jpg 112w,
                            https://i.roamcdn.net/hz/ed/listing-thumb-224w/04b5375ca21184b4dde2027303d970a8/-/horizon-files-prod/ed/picture/qenq4ev9/73f70842ddaed70d34872e9cdcd9c424b2d87aaf.jpg 224w,
                            https://i.roamcdn.net/hz/ed/listing-thumb-180w/50c3ebea639c3be0f1725244f83571bb/-/horizon-files-prod/ed/picture/qenq4ev9/73f70842ddaed70d34872e9cdcd9c424b2d87aaf.jpg 180w,
                            https://i.roamcdn.net/hz/ed/listing-thumb-360w/7ba6f0f262b2646cfc376b874ebc39db/-/horizon-files-prod/ed/picture/qenq4ev9/73f70842ddaed70d34872e9cdcd9c424b2d87aaf.jpg 360w
                          "
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div class="listing-card__content 1">
                  <div class="listing-card__content__inner">
                    <div class="listing-card__header">
                      <div class="listing-card__header-content">
                        <div class="listing-card__header__title">
                          Centre d'Appels
                        </div>
                        <div
                          class="listing-card__header__tags"
                        ></div>
                        <div class="listing-card__header__location">
                          <svg class="i i-gmaps" aria-hidden="true">
                            <use
                              xlink:href="https://www.test-site.com/assets/ed-site/icons/map.acdc5323.svg#gmaps"
                            ></use>
                          </svg>
                          Liberte 6 extension, Dakar
                        </div>
                      </div>
                    </div>
                    <div class="listing-card__date-line">
                      <div class="listing-card__header__date">
                        Hier, 10:49
                      </div> 
                      <div class='price'>100 000 FCA </div>
                    </div>
                  </div>
                </div></a
              >
                                        <a href="tel:221787320433"></a>
                          <a href="whatsapp:221787320433"></a>
                          <a href="whatsapp:phone=221007320433?message=..."></a>
                          <a href="phone:221787320433"></a>
            </div>
          </div>"""
          
item = MainItem.parse(Selector(text=html))

def test_field_ProductTitle():
    """
    This test function checks if the 'ProductTitle' field of the item matches the expected value 'Centre d'Appels'.
    """
    field = item.ProductTitle
    expected = "Centre d'Appels"
    assert field == expected

def test_field_PublishDate():
    """
    This test function checks if the 'PublishDate' field of the item has a length of 19 characters.
    """
    field = item.PublishDate
    assert len(field) == 19

def test_field_Contact():
    """
    This test function checks if the 'Contact' field of the item consists of only numeric characters separated by semicolons.
    """
    field = item.Contact
    assert all([s.isnumeric() for s in field.split(';')])

def test_field_PublishLink():
    """
    This test function checks if the 'PublishLink' field of the item matches the expected value 'https://www.test-site.com/annonce/centre-dappels-6056386'.
    """
    field = item.PublishLink
    expected = 'https://www.test-site.com/annonce/centre-dappels-6056386'
    assert expected == field

def test_field_ProductPrice():
    """
    This test function checks if the 'ProductPrice' field of the item consists of only numeric characters separated by semicolons.
    """
    field = item.ProductPrice
    assert all([s.isnumeric() for s in field.split(';')])

def test_field_VendorLocation():
    """
    This test function checks if the 'VendorLocation' field of the item matches the expected value 'Liberte 6 extension, Dakar'.
    """
    field = item.VendorLocation 
    expected = 'Liberte 6 extension, Dakar'
    assert field == expected