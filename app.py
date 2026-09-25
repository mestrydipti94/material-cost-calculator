from flask import Flask, render_template, request, redirect, url_for
import sqlite3


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    connection = sqlite3.connect("database.db")

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def create_tables():

    connection = get_db_connection()

    # -----------------------------------------------------
    # MATERIALS TABLE
    # -----------------------------------------------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS materials (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            unit TEXT NOT NULL,

            price REAL NOT NULL

        )
    """)


    # -----------------------------------------------------
    # CALCULATION HISTORY TABLE
    # -----------------------------------------------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            calculation_type TEXT NOT NULL,

            product_name TEXT,

            material_name TEXT NOT NULL,

            quantity REAL NOT NULL,

            total_material REAL,

            price_per_unit REAL NOT NULL,

            total_cost REAL NOT NULL

        )
    """)


    connection.commit()

    connection.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# =========================================================
# PRE-PRODUCTION CALCULATOR
# =========================================================

@app.route("/pre-production", methods=["GET", "POST"])
def pre_production():

    result = None

    error = None

    selected_method = None


    # =====================================================
    # GET REQUEST
    # =====================================================

    if request.method == "GET":

        selected_method = request.args.get(
            "method"
        )

        return render_template(
            "pre_production.html",

            selected_method=selected_method,

            result=None,

            error=None
        )


    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        action = request.form.get(
            "action"
        )


        # =================================================
        # STEP 1: SELECT CALCULATION METHOD
        # =================================================

        if action == "select_method":

            product_name = request.form.get(
                "product_name",
                ""
            )

            production_quantity = request.form.get(
                "production_quantity",
                ""
            )

            material_name = request.form.get(
                "material_name",
                ""
            )

            unit = request.form.get(
                "unit",
                ""
            )

            calculation_method = request.form.get(
                "calculation_method",
                ""
            )


            # -------------------------------------------------
            # VALIDATE METHOD
            # -------------------------------------------------

            if not calculation_method:

                return render_template(
                    "pre_production.html",

                    selected_method=None,

                    product_name=product_name,

                    production_quantity=production_quantity,

                    material_name=material_name,

                    unit=unit,

                    result=None,

                    error="Please select a calculation method."
                )


            # -------------------------------------------------
            # SHOW SELECTED METHOD
            # -------------------------------------------------

            return render_template(
                "pre_production.html",

                selected_method=calculation_method,

                product_name=product_name,

                production_quantity=production_quantity,

                material_name=material_name,

                unit=unit,

                result=None,

                error=None
            )


        # =================================================
        # STEP 2: CALCULATE
        # =================================================

        elif action == "calculate":

            try:

                # =========================================
                # BASIC INFORMATION
                # =========================================

                product_name = request.form[
                    "product_name"
                ].strip()


                production_quantity = float(
                    request.form[
                        "production_quantity"
                    ]
                )


                material_name = request.form[
                    "material_name"
                ].strip()


                unit = request.form[
                    "unit"
                ]


                calculation_method = request.form[
                    "calculation_method"
                ]


                # =========================================
                # VALIDATE BASIC INFORMATION
                # =========================================

                if not product_name:

                    raise ValueError(
                        "Please enter product name."
                    )


                if not material_name:

                    raise ValueError(
                        "Please enter material name."
                    )


                if production_quantity <= 0:

                    raise ValueError(
                        "Production quantity must be greater than 0."
                    )


                if not unit:

                    raise ValueError(
                        "Please select a material unit."
                    )


                # =========================================
                # MATERIAL PURCHASE INFORMATION
                # =========================================

                purchased_quantity = float(
                    request.form[
                        "purchased_quantity"
                    ]
                )


                total_material_price = float(
                    request.form[
                        "total_material_price"
                    ]
                )


                # =========================================
                # VALIDATE PURCHASE INFORMATION
                # =========================================

                if purchased_quantity <= 0:

                    raise ValueError(
                        "Purchased material quantity must be greater than 0."
                    )


                if total_material_price < 0:

                    raise ValueError(
                        "Total material price cannot be negative."
                    )


                # =========================================
                # CALCULATE PRICE PER UNIT
                # =========================================

                price_per_unit = (
                    total_material_price
                    / purchased_quantity
                )


                # =========================================
                # WASTAGE
                # =========================================

                wastage_percent = float(
                    request.form[
                        "wastage_percent"
                    ]
                )


                if wastage_percent < 0:

                    raise ValueError(
                        "Wastage percentage cannot be negative."
                    )


                # =========================================
                # MATERIAL PER PRODUCT
                # =========================================

                material_per_product = 0


                # =================================================
                # 1. MANUAL QUANTITY
                # =================================================

                if calculation_method == "manual":

                    manual_quantity = float(
                        request.form[
                            "manual_quantity"
                        ]
                    )


                    if manual_quantity <= 0:

                        raise ValueError(
                            "Material quantity must be greater than 0."
                        )


                    material_per_product = (
                        manual_quantity
                    )


                # =================================================
                # 2. AREA
                # LENGTH × WIDTH
                # =================================================

                elif calculation_method == "area":

                    length = float(
                        request.form[
                            "length"
                        ]
                    )


                    width = float(
                        request.form[
                            "width"
                        ]
                    )


                    if length <= 0:

                        raise ValueError(
                            "Length must be greater than 0."
                        )


                    if width <= 0:

                        raise ValueError(
                            "Width must be greater than 0."
                        )


                    material_per_product = (
                        length * width
                    )


                # =================================================
                # 3. VOLUME
                # LENGTH × WIDTH × HEIGHT
                # =================================================

                elif calculation_method == "volume":

                    length = float(
                        request.form[
                            "length"
                        ]
                    )


                    width = float(
                        request.form[
                            "width"
                        ]
                    )


                    height = float(
                        request.form[
                            "height"
                        ]
                    )


                    if length <= 0:

                        raise ValueError(
                            "Length must be greater than 0."
                        )


                    if width <= 0:

                        raise ValueError(
                            "Width must be greater than 0."
                        )


                    if height <= 0:

                        raise ValueError(
                            "Height must be greater than 0."
                        )


                    material_per_product = (
                        length
                        * width
                        * height
                    )


                # =================================================
                # 4. THICKNESS
                # LENGTH × WIDTH × THICKNESS
                # =================================================

                elif calculation_method == "thickness":

                    length = float(
                        request.form[
                            "length"
                        ]
                    )


                    width = float(
                        request.form[
                            "width"
                        ]
                    )


                    thickness = float(
                        request.form[
                            "thickness"
                        ]
                    )


                    if length <= 0:

                        raise ValueError(
                            "Length must be greater than 0."
                        )


                    if width <= 0:

                        raise ValueError(
                            "Width must be greater than 0."
                        )


                    if thickness <= 0:

                        raise ValueError(
                            "Thickness must be greater than 0."
                        )


                    material_per_product = (
                        length
                        * width
                        * thickness
                    )


                # =================================================
                # 5. PIECES
                # =================================================

                elif calculation_method == "pieces":

                    pieces_per_product = float(
                        request.form[
                            "pieces_per_product"
                        ]
                    )


                    if pieces_per_product <= 0:

                        raise ValueError(
                            "Pieces must be greater than 0."
                        )


                    material_per_product = (
                        pieces_per_product
                    )


                # =================================================
                # INVALID METHOD
                # =================================================

                else:

                    raise ValueError(
                        "Invalid calculation method."
                    )


                # =========================================
                # TOTAL MATERIAL
                # =========================================

                total_material = (
                    material_per_product
                    * production_quantity
                )


                # =========================================
                # WASTAGE AMOUNT
                # =========================================

                wastage_amount = (
                    total_material
                    * wastage_percent
                    / 100
                )


                # =========================================
                # FINAL MATERIAL REQUIRED
                # =========================================

                final_material = (
                    total_material
                    + wastage_amount
                )


                # =========================================
                # TOTAL COST
                # =========================================

                total_cost = (
                    final_material
                    * price_per_unit
                )


                # =========================================
                # SAVE CALCULATION TO HISTORY
                # =========================================

                connection = get_db_connection()


                connection.execute("""
                    INSERT INTO history
                    (
                        calculation_type,
                        product_name,
                        material_name,
                        quantity,
                        total_material,
                        price_per_unit,
                        total_cost
                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?)

                """, (

                    "Pre-Production",

                    product_name,

                    material_name,

                    production_quantity,

                    final_material,

                    price_per_unit,

                    total_cost

                ))


                connection.commit()

                connection.close()


                # =========================================
                # RESULT
                # =========================================

                result = {

                    "product_name":
                        product_name,

                    "production_quantity":
                        production_quantity,

                    "material_name":
                        material_name,

                    "unit":
                        unit,

                    "calculation_method":
                        calculation_method,

                    "material_per_product":
                        material_per_product,

                    "total_material":
                        total_material,

                    "wastage_percent":
                        wastage_percent,

                    "wastage_amount":
                        wastage_amount,

                    "final_material":
                        final_material,

                    "price_per_unit":
                        price_per_unit,

                    "total_cost":
                        total_cost
                }


                # =========================================
                # SHOW RESULT
                # =========================================

                return render_template(

                    "pre_production.html",

                    selected_method=
                        calculation_method,

                    product_name=
                        product_name,

                    production_quantity=
                        production_quantity,

                    material_name=
                        material_name,

                    unit=
                        unit,

                    result=
                        result,

                    error=
                        None
                )


            # =============================================
            # VALUE ERROR
            # =============================================

            except ValueError as e:

                return render_template(

                    "pre_production.html",

                    selected_method=
                        request.form.get(
                            "calculation_method"
                        ),

                    product_name=
                        request.form.get(
                            "product_name"
                        ),

                    production_quantity=
                        request.form.get(
                            "production_quantity"
                        ),

                    material_name=
                        request.form.get(
                            "material_name"
                        ),

                    unit=
                        request.form.get(
                            "unit"
                        ),

                    result=
                        None,

                    error=
                        str(e)
                )


            # =============================================
            # OTHER ERROR
            # =============================================

            except Exception as e:

                print(
                    "PRE-PRODUCTION ERROR:",
                    e
                )


                return render_template(

                    "pre_production.html",

                    selected_method=
                        request.form.get(
                            "calculation_method"
                        ),

                    product_name=
                        request.form.get(
                            "product_name"
                        ),

                    production_quantity=
                        request.form.get(
                            "production_quantity"
                        ),

                    material_name=
                        request.form.get(
                            "material_name"
                        ),

                    unit=
                        request.form.get(
                            "unit"
                        ),

                    result=
                        None,

                    error=
                        "Something went wrong. Please check your inputs."
                )


    # =====================================================
    # DEFAULT
    # =====================================================

    return render_template(

        "pre_production.html",

        selected_method=None,

        result=None,

        error=None
    )


# =========================================================
# NORMAL MATERIAL CALCULATOR
# =========================================================

@app.route(
    "/normal-calculator",
    methods=["GET", "POST"]
)
def normal_calculator():

    result = None

    error = None


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        try:

            material_name = request.form[
                "material_name"
            ].strip()


            quantity = float(
                request.form[
                    "quantity"
                ]
            )


            price_per_unit = float(
                request.form[
                    "price_per_unit"
                ]
            )


            # =============================================
            # VALIDATION
            # =============================================

            if not material_name:

                raise ValueError(
                    "Please enter material name."
                )


            if quantity <= 0:

                raise ValueError(
                    "Quantity must be greater than 0."
                )


            if price_per_unit < 0:

                raise ValueError(
                    "Price cannot be negative."
                )


            # =============================================
            # TOTAL COST
            # =============================================

            total_cost = (
                quantity
                * price_per_unit
            )


            # =============================================
            # SAVE HISTORY
            # =============================================

            connection = get_db_connection()


            connection.execute("""
                INSERT INTO history
                (
                    calculation_type,
                    product_name,
                    material_name,
                    quantity,
                    total_material,
                    price_per_unit,
                    total_cost
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                "Normal",

                None,

                material_name,

                quantity,

                quantity,

                price_per_unit,

                total_cost

            ))


            connection.commit()

            connection.close()


            # =============================================
            # RESULT
            # =============================================

            result = {

                "material_name":
                    material_name,

                "quantity":
                    quantity,

                "price_per_unit":
                    price_per_unit,

                "total_cost":
                    total_cost
            }


        except ValueError as e:

            error = str(e)


        except Exception as e:

            print(
                "NORMAL CALCULATOR ERROR:",
                e
            )

            error = (
                "Something went wrong. "
                "Please check your input."
            )


    # =====================================================
    # PAGE
    # =====================================================

    return render_template(

        "normal_calculator.html",

        result=result,

        error=error
    )


# =========================================================
# MATERIALS PAGE
# =========================================================

@app.route("/materials")
def materials():

    connection = get_db_connection()


    materials = connection.execute("""
        SELECT *

        FROM materials

        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return render_template(

        "materials.html",

        materials=materials
    )


# =========================================================
# ADD MATERIAL
# =========================================================

@app.route(
    "/add-material",
    methods=["GET", "POST"]
)
def add_material():

    error = None


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        try:

            name = request.form[
                "name"
            ].strip()


            unit = request.form[
                "unit"
            ]


            price = float(
                request.form[
                    "price"
                ]
            )


            # =============================================
            # VALIDATION
            # =============================================

            if not name:

                raise ValueError(
                    "Material name is required."
                )


            if not unit:

                raise ValueError(
                    "Please select a unit."
                )


            if price < 0:

                raise ValueError(
                    "Price cannot be negative."
                )


            # =============================================
            # INSERT MATERIAL
            # =============================================

            connection = get_db_connection()


            connection.execute("""
                INSERT INTO materials
                (
                    name,
                    unit,
                    price
                )

                VALUES (?, ?, ?)

            """, (

                name,

                unit,

                price

            ))


            connection.commit()

            connection.close()


            return redirect(
                url_for("materials")
            )


        except ValueError as e:

            error = str(e)


        except Exception as e:

            print(
                "ADD MATERIAL ERROR:",
                e
            )

            error = (
                "Unable to add material."
            )


    # =====================================================
    # PAGE
    # =====================================================

    return render_template(

        "add_material.html",

        error=error
    )


# =========================================================
# DELETE MATERIAL
# =========================================================

@app.route(
    "/delete-material/<int:id>"
)
def delete_material(id):

    connection = get_db_connection()


    connection.execute("""
        DELETE FROM materials

        WHERE id = ?

    """, (id,))


    connection.commit()

    connection.close()


    return redirect(
        url_for("materials")
    )


# =========================================================
# HISTORY PAGE
# =========================================================

@app.route("/history")
def history():

    connection = get_db_connection()


    history = connection.execute("""
        SELECT *

        FROM history

        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return render_template(

        "history.html",

        history=history
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    # Create database tables
    create_tables()

    # Start Flask server
    app.run(
        debug=True
    )