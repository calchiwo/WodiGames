#[derive(Debug)]
struct Enemy {
    x: i32,
    y: i32,
    vx: i32,
    vy: i32,
}

impl Enemy {
    fn new(x: i32, y: i32, vx: i32, vy: i32) -> Self {
        Self { x, y, vx, vy }
    }

    fn update(&mut self, width: i32, height: i32) {
        self.x += self.vx;
        self.y += self.vy;

        // Bounce on boundaries
        if self.x <= 0 || self.x >= width {
            self.vx *= -1;
        }

        if self.y <= 0 || self.y >= height {
            self.vy *= -1;
        }
    }
}

fn main() {
    let world_width = 100;
    let world_height = 50;

    let mut enemies = vec![
        Enemy::new(10, 10, 1, 1),
        Enemy::new(40, 20, -1, 1),
        Enemy::new(70, 35, 1, -1),
    ];

    println!("Starting enemy simulation...\n");

    for tick in 0..30 {
        println!("Tick {}", tick);

        for enemy in enemies.iter_mut() {
            enemy.update(world_width, world_height);
            println!("Enemy at ({}, {})", enemy.x, enemy.y);
        }

        println!("---");
    }

    println!("Simulation ended.");
}
