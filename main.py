from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

# ! TIPE DATA
class Product(BaseModel):
    idProduct: int
    name: str
    price: int
    categoryId: int
    link: str

class ProductStock(BaseModel):
    idProduct: int
    stock: int
    ukuran: str

class Category(BaseModel): 
    categoryId: int
    categoryName: str

class Discount(BaseModel):
    idProduct: int
    discount: int

class MarkUp(BaseModel):
    idProduct: int
    markUp: int

# ! READ FILE
json_filename = "Data.json"
with open(json_filename, "r") as read_file: 
    data = json.load(read_file)

# ! FAST API
app = FastAPI()

#! ROUTING Product
@app.get('/product')
async def getAllProduct():
    return data['product']

@app.get('/product/id/{idProduct}')
async def getProductById(idProduct: int):
    for product in data['product']:
        if(product['idProduct'] == idProduct):
            return product
    raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.get('/product/category/{category}')
async def getProductByCategory(category: str):
    # dapetin dulu categoryIdnya
    categoryID = -1
    found = False
    for kategori in data['category']:
        if(kategori['categoryName'] == category):
            categoryID = kategori['categoryId']
            found = True
    if found:
        productFound = False
        hasil = []
        for product in data['product']:
            if(product['categoryId'] == categoryID):
                productFound = True
                hasil.append(product)
        if productFound:
            return hasil
        if not productFound:
            return "there is no product with that category"
    if not found: 
        raise HTTPException(
		status_code=404, detail=f'category not found'
	)
    
		
    raise HTTPException(
		status_code=404, detail=f'category not found'
	)
    

@app.post('/product')
async def postProduct(product: Product):
    product_dict = product.dict()
    productFound = False
    for product in data['product']:
        if(product['idProduct']==product_dict['idProduct']):
            # ketemu product
            productFound = True
            return "Product with ID"+str(product_dict['idProduct'])+"already exist"
    if not productFound:
        data['product'].append(product_dict)
        # save ke json
        with open(json_filename, "w") as write_file: 
            json.dump(data, write_file)
        
        return product_dict
    
    raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.put('/product')
async def updateProduct(product: Product):
    product_dict = product.dict()
    productFound = False
    for product_idx, product in enumerate(data['product']):
        if(product['idProduct'] == product_dict['idProduct']):
            productFound=True
            data['product'][product_idx] = product_dict

            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            return product_dict
        
    if not productFound:
        raise HTTPException(
		status_code=404, detail=f'product not found'
	)
    
    raise HTTPException(
		status_code=404, detail=f'product not found'
	)
        
        
@app.delete('/product/{idProduct}')
async def deleteProduct(idProduct: int):
    productFound = False
    for product_idx, product in enumerate(data['product']):
        if(product['idProduct'] == idProduct):
            productFound = True
            data['product'].pop(product_idx)

            # masukkan ke dalam json
            with open(json_filename, "w") as write_file: 
                json.dump(data, write_file)
            return "Product deleted"
        
    if not productFound:
        raise HTTPException(
		status_code=404, detail=f'product not found'
	)
    
    raise HTTPException(
		status_code=404, detail=f'product not found'
	)


@app.put('/product/disc')
async def productDisc(discount: Discount):
    # TODO cari prudct yang id nya sama
    productFound = False
    discount_dict = discount.dict()
    for productIdx, product in enumerate(data['product']):
        if(product['idProduct'] == discount_dict['idProduct']):
            # TODO jika ketemu lakukan dicount terhadap product
            data['product'][productIdx]['price'] = data['product'][productIdx]['price'] - (data['product'][productIdx]['price'] * (discount_dict['discount'])/100)
            productFound = True
            # masukkan ke dalam json
            with open(json_filename, "w") as write_file: 
                json.dump(data, write_file)
            return "Data upadated"
    if not productFound:
    # TODO kalau tidak, lakukan http exception (product not found)
        raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.put('/product/markUp')
async def productMarkUp(markUp: MarkUp):
    # TODO cari prudct yang id nya sama
    productFound = False
    markup_dict = markUp.dict()
    for productIdx, product in enumerate(data['product']):
        if(product['idProduct'] == markup_dict['idProduct']):
            # TODO jika ketemu lakukan dicount terhadap product
            data['product'][productIdx]['price'] = data['product'][productIdx]['price'] + (data['product'][productIdx]['price'] * (markup_dict['markUp'])/100)
            productFound = True
            # masukkan ke dalam json
            with open(json_filename, "w") as write_file: 
                json.dump(data, write_file)
            return "Data upadated"
    if not productFound:
    # TODO kalau tidak, lakukan http exception (product not found)
        raise HTTPException(
		status_code=404, detail=f'product not found'
	)

#! ROUTING Categoy
@app.get('/category')
async def getAllcategory():
    return data['category']

@app.get('/category/{categoryId}')
async def getcategoryById(categoryId: int):
    for category in data['category']:
        if(category['categoryId'] == categoryId):
            return category
    raise HTTPException(
		status_code=404, detail=f'category not found'
	)

@app.post('/category')
async def postcategory(category: Category):
    category_dict = category.dict()
    categoryFound = False
    for category in data['category']:
        if(category['categoryId']==category_dict['categoryId']):
            # ketemu category
            categoryFound = True
            return "category with ID"+str(category_dict['categoryId'])+"already exist"
    if not categoryFound:
        data['category'].append(category_dict)
        # save ke json
        with open(json_filename, "w") as write_file: 
            json.dump(data, write_file)
        
        return category_dict
    
    raise HTTPException(
		status_code=404, detail=f'category not found'
	)

@app.put('/category')
async def updatecategory(category: Category):
    category_dict = category.dict()
    categoryFound = False
    for category_idx, category in enumerate(data['category']):
        if(category['categoryId'] == category_dict['categoryId']):
            categoryFound=True
            data['category'][category_idx] = category_dict

            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            return category_dict
        
    if not categoryFound:
        raise HTTPException(
		status_code=404, detail=f'category not found'
	)
    
    raise HTTPException(
		status_code=404, detail=f'category not found'
	)
        
        
@app.delete('/category/{categoryId}')
async def deletecategory(categoryId: int):
    categoryFound = False
    for category_idx, category in enumerate(data['category']):
        if(category['categoryId'] == categoryId):
            categoryFound = True
            data['category'].pop(category_idx)

            # masukkan ke dalam json
            with open(json_filename, "w") as write_file: 
                json.dump(data, write_file)
            return "category deleted"
        
    if not categoryFound:
        raise HTTPException(
		status_code=404, detail=f'category not found'
	)

    
    raise HTTPException(
		status_code=404, detail=f'category not found'
	)

#! ROUTING Stock
@app.get('/product_stock')
async def getAllProductStock():
    return data['product_stock']

@app.get('/product_stock/{idProduct}/{ukuran}')
async def getProductStockbyIdProductAndUkuran(idProduct: int, ukuran: str):
    for row in data['product_stock']:
        if(row['idProduct'] == idProduct and row['ukuran'] == ukuran):
            return row
    raise HTTPException(
		status_code=404, detail=f'data not found'
	)

@app.post('/product_stock')
async def postnNewRow(newRow: ProductStock):
    row_dict = newRow.dict()
    rowFound = False
    for row in data['product_stock']:
        if(row['idProduct'] == row_dict['idProduct'] and row['ukuran'] == row_dict['ukuran']):
            rowFound = True
            return "Data already exist"
    if not rowFound:
        data['product_stock'].append(row_dict)
        # save ke json
        with open(json_filename, "w") as write_file: 
            json.dump(data, write_file)
        
        return row_dict
    
    raise HTTPException(
		status_code=404, detail=f'Data not found'
	)

@app.put('/product_stock')
async def updateStock(newRow: ProductStock):
    row_dict = newRow.dict()
    rowFound = False
    for row_idx, row in enumerate(data['product_stock']):
        if(row['idProduct'] == row_dict['idProduct'] and row['ukuran'] == row_dict['ukuran']):
            rowFound=True
            data['product_stock'][row_idx] = row_dict

            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            return row_dict
        
    if not rowFound:
        raise HTTPException(
		status_code=404, detail=f'data not found'
	)
    
    raise HTTPException(
		status_code=404, detail=f'data not found'
	)