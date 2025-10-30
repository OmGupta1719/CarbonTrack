package com.example.miniproject7

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val btnSignUp = findViewById<Button>(R.id.btnSignUp)
        val btnLogin = findViewById<Button>(R.id.btnLogin)

        btnSignUp.setOnClickListener {
            startActivity(Intent(this, SignupActivity::class.java))
            // optional: finish() to prevent going back to splash
            finish()
        }

        btnLogin.setOnClickListener {
            startActivity(Intent(this, SignupActivity::class.java))
            // optional: finish() to prevent going back to splash
            finish()
        }
    }
}
