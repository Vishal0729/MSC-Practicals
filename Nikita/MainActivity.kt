package com.example.myapplication
import android.annotation.SuppressLint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.*
class MainActivity : AppCompatActivity() {

    @SuppressLint("SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val name = findViewById<EditText>(R.id.name)
        val submitButton = findViewById<Button>(R.id.button)
        val dispMessage = findViewById<TextView>(R.id.textViewResponse)

        val radioGroup = findViewById<RadioGroup>(R.id.selectgender)
        val radioB1 = findViewById<RadioButton>(R.id.radioButton1)
        val radioB2 = findViewById<RadioButton>(R.id.radioButton2)

        val checkB1 = findViewById<CheckBox>(R.id.checkBox1)
        val checkB2 = findViewById<CheckBox>(R.id.checkBox2)
        val codingLang = findViewById<TextView>(R.id.language)

        val universityYear = findViewById<Spinner>(R.id.spinner)
        val myClass = findViewById<TextView>(R.id.myclass)
        val year = arrayOf("FYCS", "SYCS", "TYCS")

        val arrayAdp = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            year
        )

        universityYear.adapter = arrayAdp

        universityYear.onItemSelectedListener =
            object : AdapterView.OnItemSelectedListener {

                @SuppressLint("SetTextI18n")
                override fun onItemSelected(
                    parent: AdapterView<*>?,
                    view: View?,
                    position: Int,
                    id: Long
                ) {
                    myClass.text = "Your Class: ${year[position]}"
                }

                @SuppressLint("SetTextI18n")
                override fun onNothingSelected(parent: AdapterView<*>?) {
                    myClass.text = "Please select your class"
                }
            }

        radioGroup.setOnCheckedChangeListener { _, checkedId ->
            when (checkedId) {
                R.id.radioButton1 ->
                    dispMessage.text = "Gender: ${radioB1.text}"

                R.id.radioButton2 ->
                    dispMessage.text = "Gender: ${radioB2.text}"
            }
        }

        submitButton.setOnClickListener {
            dispMessage.text = "Welcome ${name.text}"

            if (checkB1.isChecked && checkB2.isChecked) {
                codingLang.text = "You love both languages"
            } else if (checkB1.isChecked) {
                codingLang.text = "You love Python"
            } else if (checkB2.isChecked) {
                codingLang.text = "You love Kotlin"
            } else {
                codingLang.text = "You don't like these languages"
            }
        }
    }
}