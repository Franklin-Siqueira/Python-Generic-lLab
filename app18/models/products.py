'''
Created on Jul 13, 2019

@author: franklincarrilho
'''
from flask import Blueprint, render_template, request


productsBP = Blueprint("products", __name__, 
                 template_folder = "templates",
                 static_folder = "static")

###################################################################
#
#
#                        Product show 
#
#
###################################################################
@productsBP.route("/product/", methods = ["POST", "GET"])
def productShow():
    #
    messageHead = "Welcome to the Products Demo Page!"
    messageBody = "Your opinion about the features offered here will be really appreciated!"
    # generic product tooltips
    prodToolTipText = ["Quick View", "Add to Wishlist", "Add to Cart"]
    prodToolTipClass= ["fa fa-search", "fa fa-shopping-bag", "fa fa-shopping-cart"]
    
    # product description
    prodDescription = ["Women's Blouse", "Men's T-shirt", "Women's Blouse (2)", "Men's T-shirt (striped)"]
    # product images
    prodImgPic1 = ["http://bestjquery.com/tutorial/product-grid/demo9/images/img-1.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-3.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-5.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-7.jpg"]
    
    prodImgPic2 = ["http://bestjquery.com/tutorial/product-grid/demo9/images/img-2.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-4.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-6.jpg", 
                        "http://bestjquery.com/tutorial/product-grid/demo9/images/img-8.jpg"]
    # sale/discount labels
    prodSaleLabel= ["Sale", "Sale", "Super", "Sale"]
    prodDiscLabel= [20, 10, 5, 90]
    
    # need for loop inside for loop
    prodRating = ["*****", "***", "**", "****"]
    
    # prices
    prodPrices = [16, 20, 10, 80]
    
    # sale prices
    prodSaleVl = []
    count = 0
    for count in range(0, len(prodDescription)):
        
        prodSaleVl.append(prodPrices[count]*((100-prodDiscLabel[count])/100))
        print(prodSaleVl[count], prodDescription[count], prodImgPic1[count],"#", count)
        
                       
#                       prodPrices[2]*((100-prodDiscLabel[2])/100), 
#                       prodPrices[3]*((100-prodDiscLabel[3])/100),
#                       prodPrices[4]*((100-prodDiscLabel[4])/100)]
    
    return render_template('products1.html', 
                           productZip = zip(prodImgPic1,
                                            prodImgPic2,
                                            prodSaleLabel,
                                            prodDiscLabel,
                                            prodDescription,
                                            prodSaleVl, 
                                            prodPrices), 
                           messageHead = messageHead, 
                           message = messageBody)
#     ,       prodSaleVl))
#     , toolTipZip = zip(prodToolTipText, prodToolTipClass))
#############          end products route        ###################