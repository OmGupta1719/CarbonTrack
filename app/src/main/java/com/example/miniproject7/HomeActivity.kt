package com.example.miniproject7

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        val tv = findViewById<TextView>(R.id.tvWelcome)
        val email = intent.getStringExtra("userEmail")
        tv.text = "Welcome, ${email ?: "User"}!"
    }
}
