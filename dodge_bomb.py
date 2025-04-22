import os
import random
import sys
import pygame as pg
import time



WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
        pg.K_DOWN:(0,5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    font = pg.font.Font(None,100)
    txt = font.render("Game Over",True,(255,255,255)) 
    black_surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_surface,(0,0,0),pg.Rect(0,0,1600,800))
    black_surface.set_alpha(150) 
    kkcry_img = pg.image.load("fig/8.png")
    rkkcry_img = pg.transform.flip(kkcry_img, True, False)
    
    screen.blit(black_surface,[0,0])  
    screen.blit(rkkcry_img,[760,300])
    screen.blit(kkcry_img,[330,300])
    screen.blit(txt,[380,300])
    pg.display.update()
    time.sleep(5)
def check_bound (rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    戻り値：判定結果タプル(横、縦)
    画面内ならTrue画面外ならFalse
    """
    yoko, tate = True,True #横、縦方向用の変数
    if rct.left < 0 or WIDTH < rct.right: #画面内だったら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    #爆弾初期化
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) 
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx = 5
    vy = -5
    tmr = 0 

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):#こうかとんrectと爆弾が衝突したら
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右方向
                sum_mv[1] += mv[1]  #上下方向
        kk_rct.move_ip(sum_mv) 
        if check_bound(kk_rct) != (True,True): #画面外だったら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1]) #画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy) #爆弾の移動

        yoko,tate = check_bound(bb_rct) #爆弾の画面内判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct) #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
