from pkg.repositories import category


def get_categories():
    return category.get_categories()


def get_category_by_id(category_id: int):
    return category.get_category_by_id(category_id)


def get_category_by_name(category_name: str):
    return category.get_category_by_name(category_name)


def create_new_category(category_name: str):
    return category.create_new_category(category_name)


def update_category_by_id(category_id: int, category_name: str):
    return category.update_category_by_id(category_id, category_name)


def delete_category_by_id(category_id: int):
    return category.delete_category_by_id(category_id)
