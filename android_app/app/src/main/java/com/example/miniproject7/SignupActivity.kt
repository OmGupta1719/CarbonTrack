package com.example.miniproject7

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity

class SignupActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_signup)

        val etName = findViewById<EditText>(R.id.etName)
        val etEmail = findViewById<EditText>(R.id.etEmail)
        val etPassword = findViewById<EditText>(R.id.etPassword)
        val etConfirm = findViewById<EditText>(R.id.etConfirmPassword)
        val cb = findViewById<CheckBox>(R.id.cbTerms)
        val btnCreate = findViewById<Button>(R.id.btnCreate)
        val tvLogin = findViewById<TextView>(R.id.tvLogin)

        btnCreate.setOnClickListener {
            val name = etName.text.toString().trim()
            val email = etEmail.text.toString().trim()
            val pass = etPassword.text.toString()
            val confirm = etConfirm.text.toString()

            if (name.isEmpty() || email.isEmpty() || pass.isEmpty() || confirm.isEmpty()) {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            if (pass != confirm) {
                Toast.makeText(this, "Passwords do not match", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            if (!cb.isChecked) {
                Toast.makeText(this, "Please accept terms", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Sign-up successful: go to Home
            val intent = Intent(this, HomeActivity::class.java)
            intent.putExtra("userName", name)
            startActivity(intent)
            finish()
        }

        // Handle Android back button
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                val intent = Intent(this@SignupActivity, SplashActivity::class.java)
                startActivity(intent)
                finish()
            }
        })

        // Navigate to login screen
        tvLogin.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
}
